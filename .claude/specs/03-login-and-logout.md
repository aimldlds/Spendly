# Spec: Login and Logout

## Overview
Implement user login and logout so registered users can authenticate, start a session, and end it again. Login upgrades the existing stub `GET /login` route into a fully functional form that accepts a POST, verifies the submitted email/password against the `users` table, and establishes a Flask session on success. Logout upgrades the existing stub `GET /logout` route so it clears the session and sends the user back to the login page. Together these close the authentication loop started by Step 02 (Registration).

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`users` rows with hashed passwords exist to log in against)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — verify credentials, start session, redirect to `/profile` — public
- `GET /logout` — clear the session, redirect to `/login` — logged-in (also safe to hit while logged out; simply no-ops)

## Database changes
No new tables or columns. The existing `users` table (id, name, email, password_hash, created_at) covers all requirements.

A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — runs a parameterised `SELECT` against `users` for the given email, returns the row (or `None` if no match).

## Templates
- **Modify**: `templates/login.html`
  - Already has `method="POST"` and `action="{{ url_for('login') }}"` with `name` attributes on `email`/`password` inputs and flash message rendering — no changes required unless validation needs surfacing differently.

No new templates. Logout is a redirect-only action with no page of its own.

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST`; verify credentials, set session, add flash + redirect logic. Upgrade `logout()` to clear the session and redirect.
- `database/db.py` — add `get_user_by_email()` helper

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already available since `generate_password_hash` is in use) and Flask's built-in `session` / `flash` / `redirect` / `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- On successful login, store the user's id in `session['user_id']` (and optionally `session['user_name']` for display)
- Server-side validation must check:
  1. Both fields are non-empty
  2. Email exists in `users`
  3. Password matches the stored hash
- Use a single generic flash error ("Invalid email or password.") for both "email not found" and "wrong password" cases — never reveal which one failed, to avoid leaking which emails are registered
- On any validation failure, re-render the form with a flashed error message — do not redirect
- On successful login, `redirect` to `url_for('profile')` (no need to flash a success message since the destination page confirms login)
- Use `session.clear()` on logout to remove all session data, not just `user_id`
- Flash a confirmation message (e.g. "You have been logged out.") before redirecting on logout
- Redirect to `url_for('login')` after clearing the session
- Use `abort(405)` if an unsupported HTTP method reaches the `/login` route
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [x] `GET /login` renders the login form without errors
- [x] Submitting valid credentials sets `session['user_id']` and redirects to `/profile`
- [x] Submitting a non-existent email re-renders the form with "Invalid email or password." error, no session set
- [x] Submitting a valid email with the wrong password re-renders the form with "Invalid email or password." error, no session set
- [x] Submitting with any empty field re-renders the form with a validation error
- [x] Session persists across requests (verifiable via browser dev tools or a subsequent authenticated request)
- [x] Visiting `/logout` while logged in clears `session['user_id']` and `session['user_name']`
- [x] Visiting `/logout` redirects to `/login` with a flashed confirmation message
- [x] Visiting `/logout` while already logged out does not error — it still redirects to `/login` cleanly
- [x] After logout, the session cookie no longer grants access to logged-in-only behavior

## Status
Implemented and merged to `main` (originally as separate `03-login.md` / `04-logout.md` specs, consolidated here to match the project roadmap numbering).
