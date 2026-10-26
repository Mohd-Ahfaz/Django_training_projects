# Student Tasks — Django Project

A simple student task manager built with Django. Students can create, view, edit, complete, and delete tasks.

## Features
- Add tasks with title, description, due date, and priority
- Mark tasks as completed or pending
- Edit and delete tasks
- Search tasks by title/description
- Filter by status
- SQLite database (created automatically by Django migrations)

## Setup

Use Python 3.10+.

```bash
# 1. Open a terminal in this project folder
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create database tables
python manage.py migrate

# 4. Start the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Notes
- This is a learning/demo project. It does not include user accounts; tasks are shared on the local installation.
- For a production deployment, configure `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, authentication, and security settings.
