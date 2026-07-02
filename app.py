import os
import sqlite3
from datetime import date, datetime
from functools import wraps
from flask import Flask, render_template, g, request, redirect, url_for, flash, abort, session
from werkzeug.security import check_password_hash
from database.db import get_db, close_db, init_db, seed_db, init_app, create_user, get_user_by_email, get_expenses_for_user, create_expense, get_expense_by_id, update_expense


app = Flask(__name__)
app.secret_key = "dev"

# Configure Database
app.config['DATABASE'] = os.path.join(app.root_path, 'spendly.db')

# Register database functions with the app
init_app(app)

EXPENSE_CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please sign in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def validate_expense_input(amount, category, expense_date):
    try:
        amount_value = float(amount)
        if amount_value <= 0:
            return None, "Amount must be greater than 0."
    except ValueError:
        return None, "Amount must be a number."

    if category not in EXPENSE_CATEGORIES:
        return None, "Please select a valid category."

    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        return None, "Please enter a valid date."

    return amount_value, None


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
            return render_template("register.html")

        flash("Account created successfully. Please sign in.", "success")
        return redirect(url_for("login"))

    abort(405)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("All fields are required.", "error")
            return render_template("login.html")

        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    abort(405)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()

    if start_date and end_date and start_date > end_date:
        flash("Start date must be before end date.", "error")
        start_date = ""
        end_date = ""

    expenses = get_expenses_for_user(session["user_id"], start_date or None, end_date or None)
    total = sum(expense["amount"] for expense in expenses)
    return render_template(
        "profile.html",
        expenses=expenses,
        total=total,
        start_date=start_date,
        end_date=end_date,
    )


@app.route("/expenses/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "GET":
        return render_template(
            "expense_form.html",
            categories=EXPENSE_CATEGORIES,
            form_action=url_for("add_expense"),
            today=date.today().isoformat(),
        )

    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        amount_value, error = validate_expense_input(amount, category, expense_date)

        if error:
            flash(error, "error")
            return render_template(
                "expense_form.html",
                categories=EXPENSE_CATEGORIES,
                form_action=url_for("add_expense"),
                today=date.today().isoformat(),
                expense={
                    "amount": amount,
                    "category": category,
                    "date": expense_date,
                    "description": description,
                },
            )

        create_expense(session["user_id"], amount_value, category, expense_date, description or None)
        flash("Expense added.", "success")
        return redirect(url_for("profile"))

    abort(405)


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    expense = get_expense_by_id(id)
    if expense is None or expense["user_id"] != session["user_id"]:
        abort(404)

    if request.method == "GET":
        return render_template(
            "expense_form.html",
            categories=EXPENSE_CATEGORIES,
            form_action=url_for("edit_expense", id=id),
            today=date.today().isoformat(),
            expense=expense,
        )

    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        amount_value, error = validate_expense_input(amount, category, expense_date)

        if error:
            flash(error, "error")
            return render_template(
                "expense_form.html",
                categories=EXPENSE_CATEGORIES,
                form_action=url_for("edit_expense", id=id),
                today=date.today().isoformat(),
                expense={
                    "amount": amount,
                    "category": category,
                    "date": expense_date,
                    "description": description,
                },
            )

        update_expense(id, amount_value, category, expense_date, description or None)
        flash("Expense updated.", "success")
        return redirect(url_for("profile"))

    abort(405)


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
