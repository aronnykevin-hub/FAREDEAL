from datetime import datetime
from . import db


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False, unique=True)
	description = db.Column(db.Text, nullable=True)
	products = db.relationship("Product", backref="category", lazy=True)


class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text)
	price_cents = db.Column(db.Integer, nullable=False)
	image_url = db.Column(db.String(500))
	inventory = db.Column(db.Integer, default=0)
	is_active = db.Column(db.Boolean, default=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

