from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
"""Flask app factory and extension setup."""

db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
	app = Flask(
		__name__,
		template_folder="templates",
		static_folder="static",
	)
	app.config.from_object("supermarket_app.config.Config")

	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)

	# Import auth lazily to avoid circular imports
	from .auth import login_manager, auth_bp  # noqa: WPS433
	login_manager.init_app(app)

	# Import models so they are registered with SQLAlchemy for migrations
	from . import models  # noqa: F401

	# Register blueprints
	from .routes.catalog import catalog_bp
	from .routes.dashboard import dashboard_bp
	from .routes.inventory import inventory_bp
	from .routes.sales import sales_bp
	from .routes.deliveries import deliveries_bp
	from .routes.admin import admin_bp
	app.register_blueprint(catalog_bp)
	app.register_blueprint(dashboard_bp)
	app.register_blueprint(inventory_bp)
	app.register_blueprint(sales_bp)
	app.register_blueprint(deliveries_bp)
	app.register_blueprint(admin_bp)
	app.register_blueprint(auth_bp)

	# Redirect root to catalog
	@app.route("/")
	def index():
		return redirect(url_for("dashboard.dashboard"))

	# Ensure database tables exist on startup (simple dev convenience)
	with app.app_context():
		db.create_all()
		# Only run background scheduler off-Vercel (serverless is ephemeral)
		from .config import Config  # noqa: WPS433
		if not Config.IS_VERCEL:
			from .scheduler import start_scheduler  # noqa: WPS433
			start_scheduler(app)

	return app
