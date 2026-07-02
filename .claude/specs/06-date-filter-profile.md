# Spec: Date Filter on Profile

## Overview
Let the user narrow the expense list on `/profile` to a date range. This step adds a start-date/end-date form to the profile page that resubmits `GET /profile` with query parameters, filtering both the expense list and the total-spent figure to just that range. Consistent with the rest of the app, this is server-rendered — no JavaScript/AJAX — the page simply reloads with the filter applied.

## Depends on
- Step 05 — Backend Routes for Profile Page (`get_expenses_for_user()`, real expense list + total on `/profile`)

## Routes
- `GET /profile` — unchanged path, but now accepts optional `start_date` and `end_date` query parameters (`YYYY-MM-DD`, matching the `date` column format and HTML `<input type="date">`) and filters the expense list/total accordingly — logged-in only (unchanged from Step 04)

## Database changes
No new tables or columns.

`database/db.py`'s `get_expenses_for_user(user_id)` is extended to `get_expenses_for_user(user_id, start_date=None, end_date=None)`:
- When `start_date` is given, add `AND date >= ?` (parameterised)
- When `end_date` is given, add `AND date <= ?` (parameterised)
- Both remain optional so existing callers without a date range are unaffected

## Templates
- **Modify**: `templates/profile.html`
  - Add a filter form: two `<input type="date">` fields (`start_date`, `end_date`) and a submit button, `method="GET"` `action="{{ url_for('profile') }}"`
  - Pre-fill the inputs with the current `start_date`/`end_date` values so the filter is "sticky" across reloads
  - Show a "Clear filter" link (plain `{{ url_for('profile') }}`, no query params) only when a filter is active
  - Empty state and total-spent sections already handle the filtered list correctly since they're driven by whatever `expenses`/`total` the route passes in — no separate "no results for this range" copy needed beyond the existing empty state

## Files to change
- `app.py` — `profile()` reads `start_date`/`end_date` from `request.args`, validates them, and passes them to `get_expenses_for_user()` and back to the template
- `database/db.py` — extend `get_expenses_for_user()` with optional date-range parameters
- `templates/profile.html` — add the filter form and clear-filter link

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — date-range clauses are appended conditionally but values are always bound via `?` placeholders, never string-interpolated
- If both `start_date` and `end_date` are given and `start_date` is after `end_date`, flash an error (e.g. "Start date must be before end date.") and show the unfiltered list instead of erroring
- Query must still filter by `session['user_id']` first — the date range narrows within the user's own expenses, it never widens access
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] Submitting a start/end date on `/profile` shows only expenses within that (inclusive) range
- [ ] The total-spent figure reflects only the filtered expenses
- [ ] The date inputs stay filled with the submitted values after the page reloads
- [ ] A "Clear filter" link appears when filtered and returns to the full list when clicked
- [ ] Submitting a start date after the end date flashes a validation error and falls back to the unfiltered list
- [ ] A filtered range with no matching expenses shows the existing empty state, not an error
