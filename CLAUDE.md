# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Code Architecture and Structure

This project is a Flask-based personal expense tracking web application, named Spendly, designed as a step-by-step student project.

*   **Backend:** Developed with Python and the Flask web framework (`app.py`).
*   **Database:** Planned to use SQLite, with the database setup, initialization, and seeding logic to be implemented in `database/db.py`.
*   **Frontend:** Utilizes Jinja2 templates (`templates/`), plain CSS, and JavaScript (`static/`).
*   **Authentication:** Basic routes for `/register` and `/login` exist, with `/logout` as a placeholder.
*   **User Profile:** A placeholder route for `/profile` is present.
*   **Expense Management:** Placeholder routes for `/expenses/add`, `/expenses/<id>/edit`, and `/expenses/<id>/delete` are defined.
*   **Testing:** Uses `pytest` and `pytest-flask` for unit and integration testing.

The application currently consists mainly of UI scaffolding, with core functionality related to database interaction, user authentication (beyond basic routing), and expense management left for implementation.

## Commonly Used Commands

*   **Run the application:**
    ```bash
    python app.py
    ```
    The application will run in debug mode on port 5001.

*   **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

*   **Run tests:**
    ```bash
    pytest
    ```

*   **Run a single test:**
    ```bash
    pytest <path_to_test_file>::<test_function_name>
    ```