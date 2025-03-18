from new_backend.utils.database import db

class MedicalRecord(db.Model):
    __tablename__ = "medical_record"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # Path to uploaded file
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, patient_id, file_path):
        self.patient_id = patient_id
        self.file_path = file_path
