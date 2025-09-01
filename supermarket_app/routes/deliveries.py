from flask import Blueprint, request, render_template, redirect, url_for
from .. import db
from ..models import DeliveryOrder, Driver


deliveries_bp = Blueprint("deliveries", __name__, url_prefix="/deliveries")


@deliveries_bp.route("/")
def list_deliveries():
	orders = DeliveryOrder.query.order_by(DeliveryOrder.created_at.desc()).all()
	drivers = Driver.query.filter_by(is_active=True).order_by(Driver.full_name).all()
	return render_template("deliveries.html", orders=orders, drivers=drivers)


@deliveries_bp.route("/create", methods=["POST"])
def create_delivery():
	data = request.form
	order = DeliveryOrder(
		customer_name=data.get("customer_name", "Customer"),
		address=data.get("address", ""),
		phone=data.get("phone", ""),
		payment_cents=int(data.get("payment_cents", 0)),
	)
	db.session.add(order)
	db.session.commit()
	return redirect(url_for("deliveries.list_deliveries"))


@deliveries_bp.route("/<int:order_id>/assign", methods=["POST"])
def assign_driver(order_id: int):
	order = DeliveryOrder.query.get_or_404(order_id)
	driver_id = request.form.get("driver_id")
	order.driver_id = int(driver_id) if driver_id else None
	order.status = "assigned" if driver_id else "pending"
	db.session.commit()
	return redirect(url_for("deliveries.list_deliveries"))


@deliveries_bp.route("/<int:order_id>/status", methods=["POST"])
def update_status(order_id: int):
	order = DeliveryOrder.query.get_or_404(order_id)
	order.status = request.form.get("status", order.status)
	db.session.commit()
	return redirect(url_for("deliveries.list_deliveries"))

