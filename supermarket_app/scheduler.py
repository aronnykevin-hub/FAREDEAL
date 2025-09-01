from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from .models import Product


def start_scheduler(app):
	scheduler = BackgroundScheduler(daemon=True)

	def low_stock_check():
		with app.app_context():
			low = Product.query.filter(Product.inventory <= 5).count()
			current_app.logger.info("Low-stock items: %s", low)

	def daily_summary():
		with app.app_context():
			current_app.logger.info("Daily summary job executed")

	scheduler.add_job(low_stock_check, "interval", minutes=15, id="low_stock")
	scheduler.add_job(daily_summary, "cron", hour=21, minute=0, id="daily_summary")
	scheduler.start()
	return scheduler

