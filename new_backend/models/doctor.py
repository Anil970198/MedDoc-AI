from new_backend.utils.database import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(100), nullable=False, default="General")
    phone_number = db.Column(db.String(20), unique=True, nullable=True)  # ✅ Added phone number
