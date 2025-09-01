from flask import Blueprint, render_template
from ..models import Product
from .. import db


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def dashboard():
	product_count = db.session.query(Product).count()
	low_stock_count = db.session.query(Product).filter(Product.inventory <= 5).count()
	return render_template(
		"dashboard.html",
		stats={
			"products": product_count,
			"low_stock": low_stock_count,
			"sales_today": 0,
		}
	)

