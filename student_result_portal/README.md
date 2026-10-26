# Student Result Portal (Django)

A student result portal for managing students, subjects, marks, and result summaries.

## Features
- Dashboard with student, subject, and result statistics
- Student list, add, edit, and delete
- Subject management
- Record marks for a student in a subject
- Search students and view individual result sheets
- Calculates total marks, percentage, grade, and pass/fail status
- Django admin for managing records
- SQLite database

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the portal or http://127.0.0.1:8000/admin/ for the admin panel.

## Demo data
After migrations, you can optionally create sample records in Django admin:
1. Add a few Subjects.
2. Add Students with unique roll numbers.
3. Add Results connecting each student to each subject and enter marks.

## Grading used
- A+: 90–100%
- A: 80–89%
- B: 70–79%
- C: 60–69%
- D: 50–59%
- E: 40–49%
- F: below 40%

A subject is passed when the student earns at least 40% of its maximum marks.

## Notes
This is a college-project/demo starter. It does not include student-facing login or authorization yet. Do not use it for real student records without adding authentication, access controls, privacy protections, production settings, and appropriate institutional review.
