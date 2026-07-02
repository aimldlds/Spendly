import sqlite3
from werkzeug.security import generate_password_hash
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def seed_db():
    db = get_db()

    # Check if users table already contains data
    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        return

    # Insert demo user
    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )

    # Insert 8 sample expenses
    expenses_data = [
        (1, 50.00, "Food", "2026-06-01", "Lunch with friends"),
        (1, 25.50, "Transport", "2026-06-02", "Bus ticket"),
        (1, 75.00, "Bills", "2026-06-03", "Electricity bill"),
        (1, 120.00, "Health", "2026-06-04", "Gym membership"),
        (1, 30.00, "Entertainment", "2026-06-05", "Movie ticket"),
        (1, 80.00, "Shopping", "2026-06-06", "New shirt"),
        (1, 40.00, "Other", "2026-06-07", "Donation"),
        (1, 60.00, "Food", "2026-06-08", "Groceries"),
    ]
    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses_data,
    )
    db.commit()


def create_user(name, email, password):
    db = get_db()
    password_hash = generate_password_hash(password)
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    db.commit()
    return cursor.lastrowid


def get_user_by_email(email):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,),
    ).fetchone()


def get_expenses_for_user(user_id, start_date=None, end_date=None):
    db = get_db()
    query = "SELECT * FROM expenses WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC"
    return db.execute(query, params).fetchall()


def create_expense(user_id, amount, category, date, description):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, date, description),
    )
    db.commit()
    return cursor.lastrowid


def get_expense_by_id(expense_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,),
    ).fetchone()


def update_expense(expense_id, amount, category, date, description):
    db = get_db()
    db.execute(
        "UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ?",
        (amount, category, date, description, expense_id),
    )
    db.commit()


def delete_expense(expense_id):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()


@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('seed-db')
def seed_db_command():
    """Seed the database with sample data."""
    seed_db()
    click.echo('Seeded the database with sample data.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
