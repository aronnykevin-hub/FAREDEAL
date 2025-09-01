from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256
from .models import User
from . import db


login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
	return db.session.get(User, int(user_id))


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form.get("email", "").strip().lower()
		password = request.form.get("password", "")
		user = User.query.filter_by(email=email).first()
		if user and pbkdf2_sha256.verify(password, user.password_hash):
			login_user(user)
			return redirect(url_for("dashboard.dashboard"))
		flash("Invalid credentials", "error")
	return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("auth.login"))

