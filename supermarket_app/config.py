import os


class Config:
	SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
	SQLALCHEMY_DATABASE_URI = os.getenv(
		"DATABASE_URL",
		"sqlite:////workspace/supermarket_app/supermarket.db",
	)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
	PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")
