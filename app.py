import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from firebase_admin import credentials, initialize_app  # ✅ Import Firebase

from new_backend.utils.database import db
from new_backend.models.admin import Admin
from new_backend.models.doctor import Doctor
from new_backend.models.patient import Patient
from new_backend.models.medical_record import MedicalRecord
from new_backend.config import Config

# Import Blueprints (Routes)
from new_backend.routes.auth_routes import auth_bp
from new_backend.routes.patient_routes import patient_bp
from new_backend.routes.doctor_routes import doctor_bp
from new_backend.routes.file_routes import file_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# ✅ Initialize Firebase with Credentials from .env
firebase_credentials_path = app.config["FIREBASE_CREDENTIALS"]
if os.path.exists(firebase_credentials_path):
    cred = credentials.Certificate(firebase_credentials_path)
    initialize_app(cred)
    print("✅ Firebase Initialized")
else:
    raise FileNotFoundError(f"Firebase credentials file '{firebase_credentials_path}' not found!")

# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(patient_bp, url_prefix="/api/patients")
app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
app.register_blueprint(file_bp, url_prefix="/api/files")

if __name__ == "__main__":
    app.run(debug=True)
