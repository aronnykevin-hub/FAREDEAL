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


class Supplier(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False, unique=True)
	email = db.Column(db.String(200))
	phone = db.Column(db.String(50))
	address = db.Column(db.String(300))
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	purchase_orders = db.relationship("PurchaseOrder", backref="supplier", lazy=True)


class StockMovement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
	delta = db.Column(db.Integer, nullable=False)
	reason = db.Column(db.String(100), default="adjustment")
	created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SaleTransaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	total_cents = db.Column(db.Integer, default=0)
	items = db.relationship("SaleItem", backref="sale", lazy=True, cascade="all, delete-orphan")


class SaleItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sale_id = db.Column(db.Integer, db.ForeignKey("sale_transaction.id"), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	price_cents = db.Column(db.Integer, nullable=False)
	line_total_cents = db.Column(db.Integer, nullable=False)


class PurchaseOrder(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"), nullable=False)
	status = db.Column(db.String(50), default="draft")
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	received_at = db.Column(db.DateTime, nullable=True)
	items = db.relationship("PurchaseOrderItem", backref="purchase_order", lazy=True, cascade="all, delete-orphan")


class PurchaseOrderItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	purchase_order_id = db.Column(db.Integer, db.ForeignKey("purchase_order.id"), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	cost_cents = db.Column(db.Integer, nullable=False)


class Employee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(200), nullable=False)
	role = db.Column(db.String(50), default="staff")
	email = db.Column(db.String(200), unique=True)
	phone = db.Column(db.String(50))
	created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Shift(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
	starts_at = db.Column(db.DateTime, nullable=False)
	ends_at = db.Column(db.DateTime, nullable=False)


class Driver(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(50))
	is_active = db.Column(db.Boolean, default=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	deliveries = db.relationship("DeliveryOrder", backref="driver", lazy=True)


class DeliveryOrder(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	customer_name = db.Column(db.String(200), nullable=False)
	address = db.Column(db.String(300), nullable=False)
	phone = db.Column(db.String(50))
	status = db.Column(db.String(50), default="pending")
	driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	payment_cents = db.Column(db.Integer, default=0)


