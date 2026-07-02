# Spec: Profile Page

## Overview
Build the authenticated shell of the app: the `/profile` route becomes a real, login-gated page that greets the signed-in user and reserves a section for their expenses. This step establishes the auth-guard pattern (`login_required`) that this route and later logged-in-only routes (add/edit/delete expense) will reuse, and gives the navbar a logged-in state. Actual expense data and totals are wired up in Step 05 (Backend Routes for Profile Page) — this step renders the page structure with the data that's already available (the session).

## Depends on
- Step 01 — Database setup (`users` table)
- Step 03 — Login and Logout (`session['user_id']` / `session['user_name']` set on login, cleared on logout)

## Routes
- `GET /profile` — render the profile page for the signed-in user — logged-in only. Unauthenticated visitors are redirected to `/login` with a flashed message.

## Database changes
No database changes. This step only reads `session['user_id']` / `session['user_name']`; it does not query `expenses` yet (that's Step 05).

## Templates
- **Create**: `templates/profile.html`
  - Extends `base.html`
  - Shows a header greeting with the user's name (from `session['user_name']`)
  - Includes an expenses section with a placeholder state (e.g. "No expenses yet" / "Your expenses will appear here") — Step 05 replaces this placeholder with the real, data-driven list
- **Modify**: `templates/base.html`
  - Navbar shows "Sign in" / "Get started" when logged out (current behavior)
  - Navbar shows "Profile" / "Logout" links when `session['user_id']` is present

## Files to change
- `app.py`
  - Add a `login_required` decorator that checks `session['user_id']`; if missing, flash a message (e.g. "Please sign in to continue.") and redirect to `/login`
  - Upgrade `profile()` to use `@login_required` and render `templates/profile.html`
- `templates/base.html` — conditional navbar links based on session state

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL (n/a — no queries in this step)
- `login_required` must be a decorator (`functools.wraps`), not copy-pasted checks, since it will be reused by Steps 07–09
- Use `session.get('user_id')` — never assume the key exists
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login` with a flashed message, no error
- [ ] Visiting `/profile` while logged in renders the page and greets the user by name
- [ ] Navbar shows "Profile" / "Logout" instead of "Sign in" / "Get started" when logged in
- [ ] Logging out and revisiting `/profile` redirects to `/login` again
