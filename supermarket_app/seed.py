from passlib.hash import pbkdf2_sha256
from . import db
from .models import Category, Product, User, Driver


def seed(app):
	with app.app_context():
		if not User.query.filter_by(email="admin@faredeal.local").first():
			admin = User(
				full_name="Admin",
				email="admin@faredeal.local",
				password_hash=pbkdf2_sha256.hash("admin123"),
				role="admin",
			)
			db.session.add(admin)

		if Category.query.count() == 0:
			produce = Category(name="Produce")
			dairy = Category(name="Dairy")
			db.session.add_all([produce, dairy])
			db.session.flush()
			db.session.add_all([
				Product(name="Bananas", price_cents=199, inventory=120, category=produce),
				Product(name="Milk 1L", price_cents=249, inventory=60, category=dairy),
			])

		if Driver.query.count() == 0:
			db.session.add_all([
				Driver(full_name="Alice Driver", phone="+1000001"),
				Driver(full_name="Bob Courier", phone="+1000002"),
			])

		db.session.commit()

