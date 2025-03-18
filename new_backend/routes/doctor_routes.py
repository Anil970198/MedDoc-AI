from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required
from new_backend.utils.database import db
from new_backend.models.doctor import Doctor

bcrypt = Bcrypt()

doctor_bp = Blueprint('doctor', __name__, url_prefix="/api/doctors")

# ✅ Add a new doctor
@doctor_bp.route('', methods=['POST'])
@jwt_required()
def add_doctor():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    specialization = data.get("specialization")

    if not name or not email or not password or not specialization:
        return jsonify({"error": "Missing required fields"}), 400

    # ✅ Check if the email already exists
    existing_doctor = Doctor.query.filter_by(email=email).first()
    if existing_doctor:
        return jsonify({"error": "A doctor with this email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_doctor = Doctor(name=name, email=email, password=hashed_password, specialization=specialization)

    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({"message": "Doctor added successfully"}), 201


# ✅ Get all doctors
@doctor_bp.route('', methods=['GET'])
def get_all_doctors():
    doctors = Doctor.query.all()
    doctor_list = [{"id": d.id, "name": d.name, "email": d.email, "specialization": d.specialization} for d in doctors]

    return jsonify({"doctors": doctor_list}), 200

# ✅ Get a doctor by ID
@doctor_bp.route('/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({
        "id": doctor.id,
        "name": doctor.name,
        "email": doctor.email,
        "specialization": doctor.specialization
    }), 200

# ✅ Update a doctor's details
@doctor_bp.route('/<int:id>', methods=['PUT'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    data = request.get_json()
    doctor.name = data.get("name", doctor.name)
    doctor.email = data.get("email", doctor.email)
    doctor.specialization = data.get("specialization", doctor.specialization)

    db.session.commit()
    return jsonify({"message": "Doctor updated successfully"}), 200

# ✅ Delete a doctor
@doctor_bp.route('/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"message": "Doctor deleted successfully"}), 200
