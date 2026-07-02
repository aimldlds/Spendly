# Spec: Edit Expense

## Overview
Let a signed-in user edit one of their existing expenses. This step upgrades the existing stub `GET /expenses/<id>/edit` route into a form pre-filled with the expense's current values, reusing the `templates/expense_form.html` built in Step 07. On success the expense is updated in place and the user is redirected to `/profile`.

## Depends on
- Step 05 — Backend Routes for Profile Page (expenses listed on `/profile`)
- Step 07 — Add Expense (`EXPENSE_CATEGORIES`, `templates/expense_form.html`, validation pattern)

## Routes
- `GET /expenses/<int:id>/edit` — render the edit form pre-filled with the expense's data — logged-in only, and the expense must belong to the signed-in user
- `POST /expenses/<int:id>/edit` — validate and update the expense, redirect to `/profile` — logged-in only, same ownership check

## Database changes
No new tables or columns.

Two new DB helpers must be added to `database/db.py`:
- `get_expense_by_id(expense_id)` — parameterised `SELECT * FROM expenses WHERE id = ?`, returns the row or `None`
- `update_expense(expense_id, amount, category, date, description)` — parameterised `UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ?`

## Templates
- **Modify**: none required — `templates/expense_form.html` (Step 07) already branches on whether an `expense` variable is present to switch between "Add expense" and "Edit expense" copy and pre-fill values. This step just passes `expense` and `form_action` pointing at the edit route.

## Files to change
- `app.py` — upgrade `edit_expense(id)` to handle `GET` and `POST`, with ownership checks and the same validation rules as `add_expense`
- `database/db.py` — add `get_expense_by_id()` and `update_expense()` helpers

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Route must be decorated with `@login_required`
- Ownership check: if the expense doesn't exist, or its `user_id` doesn't match `session['user_id']`, respond with `abort(404)` — never reveal whether an expense id belongs to someone else
- Reuse the same validation rules as Step 07 (`add_expense`): amount numeric and > 0, category in `EXPENSE_CATEGORIES`, date matches `YYYY-MM-DD`
- On any validation failure, re-render the form with a flashed error message and the submitted values preserved — do not redirect
- On success, flash a confirmation (e.g. "Expense updated.") and redirect to `url_for('profile')`
- The expense's `user_id` is never changed and never taken from form input
- Use `abort(405)` if an unsupported HTTP method reaches the route
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] Visiting `/expenses/<id>/edit` while logged out redirects to `/login`
- [ ] Visiting `/expenses/<id>/edit` for an expense that doesn't exist returns 404
- [ ] Visiting `/expenses/<id>/edit` for another user's expense returns 404 (verifiable by seeding a second user with their own expense)
- [ ] `GET /expenses/<id>/edit` for your own expense renders the form pre-filled with its current values
- [ ] Submitting valid changes updates the row and redirects to `/profile`, where the updated values appear
- [ ] Submitting invalid input (bad amount/category/date) re-renders the form with a validation error, no update applied
