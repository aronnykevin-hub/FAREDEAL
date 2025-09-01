import os


class Config:
	IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))
	SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
	SQLALCHEMY_DATABASE_URI = os.getenv(
		"DATABASE_URL",
		(
			"sqlite:////tmp/supermarket.db"
			if IS_VERCEL
			else "sqlite:////workspace/supermarket_app/supermarket.db"
		),
	)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
	PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")
