from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

	# Import models so they are registered with SQLAlchemy for migrations
	from . import models  # noqa: F401

	# Register blueprints
	from .routes.catalog import catalog_bp
	from .routes.dashboard import dashboard_bp
	from .routes.inventory import inventory_bp
	from .routes.sales import sales_bp
	from .routes.deliveries import deliveries_bp
	app.register_blueprint(catalog_bp)
	app.register_blueprint(dashboard_bp)
	app.register_blueprint(inventory_bp)
	app.register_blueprint(sales_bp)
	app.register_blueprint(deliveries_bp)

	# Redirect root to catalog
	@app.route("/")
	def index():
		return redirect(url_for("dashboard.dashboard"))

	# Ensure database tables exist on startup (simple dev convenience)
	with app.app_context():
		db.create_all()

	return app
