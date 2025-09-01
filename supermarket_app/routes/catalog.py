from flask import Blueprint, render_template
from ..models import Product, Category


catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")


@catalog_bp.route("/")
def catalog():
	categories = Category.query.order_by(Category.name).all()
	products = (
		Product.query.filter_by(is_active=True).order_by(Product.name).all()
	)
	return render_template("catalog.html", categories=categories, products=products)

