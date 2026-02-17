import os


class Config:
    """Application configuration shared across environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///erp_local.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
