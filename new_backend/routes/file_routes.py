import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from new_backend.utils.database import db
from new_backend.models.medical_record import MedicalRecord
from new_backend.models.patient import Patient  # ✅ Import Patient model to check if the patient exists

file_bp = Blueprint("file", __name__, url_prefix="/api/files")

# Define the upload directory
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ✅ API to Upload Medical Records
@file_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_medical_record():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    patient_id = request.form.get("patient_id")

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF, PNG, JPG, and JPEG allowed"}), 400

    if not patient_id:
        return jsonify({"error": "Missing patient_id"}), 400

    # ✅ Convert patient_id to an integer
    try:
        patient_id = int(patient_id)
    except ValueError:
        return jsonify({"error": "Invalid patient_id"}), 400

    # ✅ Ensure the patient exists
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Secure and save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Store record in the database
    new_record = MedicalRecord(patient_id=patient_id, file_path=filepath)
    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "file_path": filepath}), 201


# ✅ API to Get Medical Records by Patient ID
@file_bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_medical_records(patient_id):
    """Retrieve all medical records for a specific patient."""

    # ✅ Ensure the patient exists
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()

    if not records:
        return jsonify({"message": "No records found for this patient"}), 404

    record_list = [{"id": r.id, "file_path": r.file_path, "uploaded_at": r.uploaded_at} for r in records]

    return jsonify({"records": record_list}), 200
