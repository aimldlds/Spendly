# Spec: Logout

## Overview
Implement user logout so an authenticated user can end their session. This step upgrades the existing stub `GET /logout` route so it clears the Flask session and sends the user back to the login page. This closes the authentication loop started by Step 02 (Registration) and Step 03 (Login).

## Depends on
- Step 03 — Login (`session['user_id']` must exist for there to be anything to log out of)

## Routes
- `GET /logout` — clear the session, redirect to `/login` — logged-in (also safe to hit while logged out; simply no-ops)

## Database changes
No database changes.

## Templates
No new templates. No modifications required — logout is a redirect-only action with no page of its own.

## Files to change
- `app.py` — upgrade `logout()` to clear the session and redirect

## Files to create
None.

## New dependencies
No new dependencies. Uses Flask's built-in `session` / `redirect` / `url_for` / `flash`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL (n/a here, no queries)
- Use `session.clear()` to remove all session data, not just `user_id`
- Flash a confirmation message (e.g. "You have been logged out.") before redirecting
- Redirect to `url_for('login')` after clearing the session
- Use `url_for()` for every internal link — never hardcode URLs
- All templates extend `base.html` (n/a — no template changes in this step)

## Definition of done
- [ ] Visiting `/logout` while logged in clears `session['user_id']` and `session['user_name']`
- [ ] Visiting `/logout` redirects to `/login` with a flashed confirmation message
- [ ] Visiting `/logout` while already logged out does not error — it still redirects to `/login` cleanly
- [ ] After logout, the session cookie no longer grants access to logged-in-only behavior
