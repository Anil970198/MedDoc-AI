from flask import Blueprint, request, jsonify
from new_backend.utils.database import db
from new_backend.models.patient import Patient

patient_bp = Blueprint('patient', __name__, url_prefix="/api/patients")


# ✅ Add a new patient
@patient_bp.route('', methods=['POST'])
def add_patient():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    medical_history = data.get("medical_history", "")

    if not name or not email or not age:
        return jsonify({"error": "Missing required fields"}), 400

    new_patient = Patient(name=name, email=email, age=age, medical_history=medical_history)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "Patient added successfully", "patient_id": new_patient.id}), 201


# ✅ Get all patients
@patient_bp.route('', methods=['GET'])
def get_all_patients():
    patients = Patient.query.all()
    patients_list = [{"id": p.id, "name": p.name, "email": p.email, "age": p.age, "medical_history": p.medical_history}
                     for p in patients]

    return jsonify({"patients": patients_list}), 200


# ✅ Get a patient by ID
@patient_bp.route('/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "email": patient.email,
        "age": patient.age,
        "medical_history": patient.medical_history
    }), 200


# ✅ Update a patient's details
@patient_bp.route('/<int:id>', methods=['PUT'])
def update_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()
    patient.name = data.get("name", patient.name)
    patient.email = data.get("email", patient.email)
    patient.age = data.get("age", patient.age)
    patient.medical_history = data.get("medical_history", patient.medical_history)

    db.session.commit()
    return jsonify({"message": "Patient updated successfully"}), 200


# ✅ Delete a patient
@patient_bp.route('/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"}), 200


