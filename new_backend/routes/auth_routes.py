import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import firebase_admin
from firebase_admin import auth

from new_backend.utils.database import db
from new_backend.models.admin import Admin
from new_backend.models.doctor import Doctor
from new_backend.models.patient import Patient

auth_bp = Blueprint('auth', __name__)

# ✅ Find user in all tables
def find_user(phone_number):
    return (Admin.query.filter_by(phone_number=phone_number).first() or
            Doctor.query.filter_by(phone_number=phone_number).first() or
            Patient.query.filter_by(phone_number=phone_number).first())

# ✅ Request OTP (Firebase will handle OTP generation & SMS)
@auth_bp.route('/request-otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    phone_number = data.get("phone_number")

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    user = find_user(phone_number)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        # ✅ Request OTP via Firebase
        verification = auth.create_custom_token(phone_number)
        return jsonify({"message": "OTP request successful", "custom_token": verification.decode()}), 200
    except Exception as e:
        return jsonify({"error": f"Firebase OTP Error: {str(e)}"}), 500

# ✅ Verify OTP (User must enter OTP sent via Firebase)
@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone_number = data.get("phone_number")
    id_token = data.get("id_token")  # Token received after OTP verification

    if not phone_number or not id_token:
        return jsonify({"error": "Phone number and OTP token required"}), 400

    user = find_user(phone_number)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        # ✅ Verify OTP using Firebase
        decoded_token = auth.verify_id_token(id_token)
        if decoded_token["phone_number"] != phone_number:
            return jsonify({"error": "Invalid OTP"}), 401

        # ✅ Generate JWT Token after successful OTP verification
        access_token = create_access_token(identity=phone_number)
        return jsonify({"access_token": access_token, "message": "Login successful"}), 200
    except Exception as e:
        return jsonify({"error": f"Firebase Verification Error: {str(e)}"}), 500

# ✅ Protected Route (Only Accessible with Valid Token)
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome, {current_user}! You accessed a protected route."}), 200
