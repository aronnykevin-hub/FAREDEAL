from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from .. import db
from ..models import Product, Category


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/products")
@login_required
def products():
	products = Product.query.order_by(Product.name).all()
	categories = Category.query.order_by(Category.name).all()
	return render_template("admin_products.html", products=products, categories=categories)


@admin_bp.route("/products/create", methods=["POST"])
@login_required
def create_product():
	form = request.form
	product = Product(
		name=form.get("name"),
		description=form.get("description"),
		price_cents=int(form.get("price_cents", 0)),
		image_url=form.get("image_url"),
		inventory=int(form.get("inventory", 0)),
		category_id=int(form.get("category_id")) if form.get("category_id") else None,
		barcode=form.get("barcode") or None,
	)
	db.session.add(product)
	db.session.commit()
	return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id: int):
	product = Product.query.get_or_404(product_id)
	db.session.delete(product)
	db.session.commit()
	return redirect(url_for("admin.products"))


@admin_bp.route("/categories")
@login_required
def categories():
	categories = Category.query.order_by(Category.name).all()
	return render_template("admin_categories.html", categories=categories)


@admin_bp.route("/categories/create", methods=["POST"])
@login_required
def create_category():
	form = request.form
	category = Category(name=form.get("name"), description=form.get("description"))
	db.session.add(category)
	db.session.commit()
	return redirect(url_for("admin.categories"))


@admin_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id: int):
	category = Category.query.get_or_404(category_id)
	db.session.delete(category)
	db.session.commit()
	return redirect(url_for("admin.categories"))

