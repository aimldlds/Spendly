# Spec: Delete Expense

## Overview
Let a signed-in user delete one of their own expenses. This step upgrades the existing stub `GET /expenses/<id>/delete` route into a `POST`-only action (deletion is destructive, so it must never be triggerable by a plain link/GET request or link prefetching) and adds Edit/Delete action links to each row on `/profile`, which Step 05 deliberately left out until this step existed.

## Depends on
- Step 05 — Backend Routes for Profile Page (expense rows rendered on `/profile`)
- Step 08 — Edit Expense (ownership-check pattern, `EXPENSE_CATEGORIES`)

## Routes
- `POST /expenses/<int:id>/delete` — delete the expense, redirect to `/profile` — logged-in only, and the expense must belong to the signed-in user. `GET` on this path is no longer supported.

## Database changes
No new tables or columns.

A new DB helper must be added to `database/db.py`:
- `delete_expense(expense_id)` — parameterised `DELETE FROM expenses WHERE id = ?`

## Templates
- **Modify**: `templates/profile.html`
  - Each expense row gets an "Edit" link (`GET` to `url_for('edit_expense', id=expense.id)`) and a "Delete" button inside a small `POST` form (`action="{{ url_for('delete_expense', id=expense.id) }}"`)
  - The delete form is confirmed client-side before submitting (see `static/js/main.js`) so a misclick can't silently delete data

## Files to change
- `app.py` — upgrade `delete_expense(id)`: `POST`-only, ownership check, delete, flash, redirect
- `database/db.py` — add `delete_expense()` helper
- `templates/profile.html` — add Edit/Delete actions per row
- `static/css/style.css` — minimal styling for the new row actions
- `static/js/main.js` — attach a `confirm()` prompt to delete forms before they submit

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Route must be decorated with `@login_required` and declared with `methods=["POST"]` only — no `GET` handler, use `abort(405)` for any other method
- Ownership check: if the expense doesn't exist, or its `user_id` doesn't match `session['user_id']`, respond with `abort(404)` — same pattern as Step 08's edit route
- Deletion must be confirmed client-side (`confirm()`) before the form submits, to guard against accidental clicks
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] `GET /expenses/<id>/delete` is no longer a valid request (405, not a text placeholder)
- [ ] `POST /expenses/<id>/delete` while logged out redirects to `/login`
- [ ] `POST /expenses/<id>/delete` for an expense that doesn't exist, or belongs to another user, returns 404 and deletes nothing
- [ ] `POST /expenses/<id>/delete` for your own expense removes it from `expenses` and redirects to `/profile`, where it no longer appears and the total reflects the removal
- [ ] Clicking "Delete" on `/profile` shows a confirmation prompt before the request is sent
- [ ] Deleting a user's only expense correctly falls back to the "No expenses yet" empty state
