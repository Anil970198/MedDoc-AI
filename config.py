class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://meddoc_user:anianu@localhost/meddoc_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Load environment variables from .env
    import os
    from dotenv import load_dotenv
    load_dotenv()

    DB_USER = os.getenv("DB_USER", "meddoc_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_database_password")
    DB_NAME = os.getenv("DB_NAME", "meddoc_db")
    DB_HOST = os.getenv("DB_HOST", "localhost")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configurations (Fixing the Issue)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")  # Ensure you have a valid JWT key
    JWT_TOKEN_LOCATION = ["headers"]  # Ensures token is fetched from headers
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    SECRET_KEY = os.getenv("SECRET_KEY")

    # Twilio Config

    # Firebase Config
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "firebase_key.json")