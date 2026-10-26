# Employee Salary Slip — Django Project

A Django web application for maintaining employee details, preparing monthly salary slips, calculating earnings/deductions, and printing slips.

## Features
- Dashboard with employee and salary-slip totals
- Employee add, edit, view, and delete
- Monthly salary records
- Earnings: basic salary, HRA, allowances, bonus
- Deductions: PF, tax, other deductions
- Automatic gross salary, total deductions, and net salary calculation
- Search employees and filter slips by month/year
- Print-friendly salary slip
- Django admin and SQLite database

## Setup
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

Open http://127.0.0.1:8000/ for the app and http://127.0.0.1:8000/admin/ for the admin panel.

## Usage
1. Add employee details.
2. Choose "Create salary slip".
3. Select the employee and pay period, then enter earnings and deductions.
4. Open the slip and use "Print salary slip" to print or save as PDF from your browser.

## Important
This is a learning/demo project. Payroll rules vary by location and employer. The calculations are simple totals, not tax/legal advice. Before using with real payroll data, add authentication and role-based access, secure production settings, audit logs, and validate deductions against applicable law and company policy. Do not use the demo secret key or DEBUG=True in production.
