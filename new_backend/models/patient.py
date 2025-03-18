from new_backend.utils.database import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)  # ✅ Added phone number
