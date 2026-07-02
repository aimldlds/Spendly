# Spec: Add Expense

## Overview
Let a signed-in user record a new expense. This step upgrades the existing stub `GET /expenses/add` route into a fully functional form that accepts a POST, validates input, and inserts a new row into `expenses` for the signed-in user. On success the user is redirected to `/profile` where the new expense appears in their list and total.

## Depends on
- Step 01 — Database setup (`expenses` table)
- Step 04 — Profile Page (`login_required` decorator)
- Step 05 — Backend Routes for Profile Page (expenses show up on `/profile` once inserted)

## Routes
- `GET /expenses/add` — render the add-expense form — logged-in only (already exists as stub, upgrade it)
- `POST /expenses/add` — validate and insert the expense, redirect to `/profile` — logged-in only

## Database changes
No new tables or columns. The existing `expenses` table (id, user_id, amount, category, date, description, created_at) covers all requirements.

A new DB helper must be added to `database/db.py`:
- `create_expense(user_id, amount, category, date, description)` — parameterised `INSERT` into `expenses`, returns the new row's `id`.

## Categories
The category field is a fixed dropdown, not free text, matching the categories already used by seeded data: `Food`, `Transport`, `Bills`, `Health`, `Entertainment`, `Shopping`, `Other`. Define this list once in `app.py` as `EXPENSE_CATEGORIES` so Step 08 (Edit Expense) can reuse it instead of duplicating.

## Templates
- **Create**: `templates/expense_form.html`
  - Extends `base.html`
  - Form fields: `amount` (number input, step 0.01, min 0.01), `category` (select, populated from `EXPENSE_CATEGORIES`), `date` (date input), `description` (text input, optional)
  - Flash error display (reuse the `auth-error`/`auth-success` pattern already used elsewhere)
  - Designed to be reused by Step 08 (Edit Expense) — accepts an optional `expense` variable to pre-fill fields when editing; when absent (add mode) fields start empty except `date`, which defaults to today

## Files to change
- `app.py` — upgrade `add_expense()` to handle `GET` and `POST`; add `EXPENSE_CATEGORIES` constant; add validation + flash + redirect logic
- `database/db.py` — add `create_expense()` helper

## Files to create
- `templates/expense_form.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Route must be decorated with `@login_required`
- Server-side validation must check:
  1. `amount` is present, numeric, and greater than 0
  2. `category` is present and is one of `EXPENSE_CATEGORIES`
  3. `date` is present and matches `YYYY-MM-DD`
  4. `description` is optional
- On any validation failure, re-render the form with a flashed error message and the submitted values preserved — do not redirect
- On success, flash a confirmation (e.g. "Expense added.") and redirect to `url_for('profile')`
- The inserted expense's `user_id` must always come from `session['user_id']` — never from form input, so a user can never add an expense on another user's behalf
- Use `abort(405)` if an unsupported HTTP method reaches the route
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] Visiting `/expenses/add` while logged out redirects to `/login` (via existing `login_required`)
- [ ] `GET /expenses/add` renders the form with today's date pre-filled
- [ ] Submitting a valid expense inserts a row into `expenses` for the current user and redirects to `/profile`, where it appears in the list and total
- [ ] Submitting with a missing/zero/negative amount re-renders the form with a validation error, no insert
- [ ] Submitting with an invalid category re-renders the form with a validation error, no insert
- [ ] Submitting with a missing date re-renders the form with a validation error, no insert
- [ ] The new expense's `user_id` always matches the logged-in user, regardless of form input
