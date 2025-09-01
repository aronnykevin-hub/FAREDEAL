from flask import Blueprint, request, jsonify
from .. import db
from ..models import Product, SaleTransaction, SaleItem


sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


@sales_bp.route("/create", methods=["POST"])
def create_sale():
	data = request.get_json(force=True, silent=True) or {}
	items = data.get("items", [])
	if not items:
		return jsonify({"error": "No items"}), 400

	sale = SaleTransaction()
	db.session.add(sale)
	total_cents = 0
	for item in items:
		product = Product.query.get(item.get("product_id"))
		qty = int(item.get("quantity", 1))
		if not product or qty <= 0:
			continue
		line_total = product.price_cents * qty
		total_cents += line_total
		sale_item = SaleItem(
			sale=sale,
			product_id=product.id,
			quantity=qty,
			price_cents=product.price_cents,
			line_total_cents=line_total,
		)
		db.session.add(sale_item)
		product.inventory = (product.inventory or 0) - qty

	sale.total_cents = total_cents
	db.session.commit()
	return jsonify({"sale_id": sale.id, "total_cents": total_cents}), 201

