# Spec: Backend Routes for Profile Page

## Overview
Wire real data into the profile page. Step 04 built the page shell with a static placeholder; this step replaces that placeholder by querying the signed-in user's expenses from the database and rendering them with a running total. No new routes are needed — `GET /profile` is upgraded to fetch and pass real data to the existing template.

## Depends on
- Step 01 — Database setup (`expenses` table)
- Step 03 — Login and Logout (`session['user_id']`)
- Step 04 — Profile Page (`/profile` route, `login_required`, `templates/profile.html` shell)

## Routes
No new routes. `GET /profile` (already login-gated) now queries and renders real expense data instead of the static placeholder.

## Database changes
No new tables or columns.

A new DB helper must be added to `database/db.py`:
- `get_expenses_for_user(user_id)` — parameterised `SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC`, returns all matching rows.

Total spent is computed in Python (`sum()` over the returned rows) rather than a second query, to keep this step to a single DB round trip.

## Templates
- **Modify**: `templates/profile.html`
  - Add a total-spent summary (e.g. a stat showing the sum of all listed expenses)
  - Replace the placeholder empty state with a real expense list: each row shows date, category, description, and amount
  - If the user has zero expenses, keep the existing "No expenses yet" empty state from Step 04

## Files to change
- `app.py` — `profile()` calls `get_expenses_for_user()`, computes the total, and passes both to the template
- `database/db.py` — add `get_expenses_for_user()` helper
- `templates/profile.html` — render the real expense list and total
- `static/css/style.css` — styles for the expense list rows and total stat (new classes, reuse existing CSS variables)

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Query must filter by `session['user_id']` — a user must never see another user's expenses
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs
- Edit/delete action links are out of scope for this step (Steps 08/09) — display only

## Definition of done
- [ ] `/profile` shows the signed-in user's expenses, most recent first
- [ ] `/profile` shows a total-spent figure that matches the sum of the listed expenses
- [ ] A user with zero expenses still sees the "No expenses yet" empty state, not an error
- [ ] Logging in as a different user shows only that user's own expenses (verifiable by seeding a second user)
