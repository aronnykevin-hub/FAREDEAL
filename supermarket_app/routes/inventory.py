from flask import Blueprint, request, redirect, url_for, render_template
from .. import db
from ..models import Product, Category, Supplier, StockMovement


inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_bp.route("/")
def inventory_home():
	products = Product.query.order_by(Product.name).all()
	return render_template("inventory.html", products=products)


@inventory_bp.route("/adjust", methods=["POST"])
def adjust_stock():
	product_id = int(request.form.get("product_id"))
	quantity = int(request.form.get("quantity", 0))
	reason = request.form.get("reason", "manual_adjust")
	product = Product.query.get_or_404(product_id)
	product.inventory = (product.inventory or 0) + quantity
	db.session.add(
		StockMovement(product_id=product.id, delta=quantity, reason=reason)
	)
	db.session.commit()
	return redirect(url_for("inventory.inventory_home"))

