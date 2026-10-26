# ATM Balance Checker (Django)

A small ATM simulator. Sign in with a card number and PIN, then check your balance,
withdraw, deposit, or view a mini statement. Built with Django + SQLite, no extra packages.

## Run it (about a minute)

```bash
# 1. (optional but recommended) virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. install Django
pip install -r requirements.txt

# 3. create the database and the demo cards
python manage.py migrate
python manage.py seed_demo

# 4. start the server, then open http://127.0.0.1:8000/
python manage.py runserver
```

## Demo cards (created by `seed_demo`)

| Name         | Card number        | PIN  | Balance     |
|--------------|--------------------|------|-------------|
| Aarav Sharma | 4111111111111111   | 1234 | ₹25,000.00  |
| Priya Verma  | 5500000000000004   | 4321 | ₹1,20,500.50|
| Rohan Singh  | 6011000000000004   | 2580 | ₹500.00     |

Running `seed_demo` again resets these three cards (balance, PIN, unlock).

## What it does

- Card number + 4-digit PIN login (PIN is stored hashed, never in plain text)
- Check balance (Indian number format, e.g. ₹1,20,500.50)
- Withdraw: multiples of ₹100, up to ₹20,000 per transaction, blocked if balance is too low
- Deposit: up to ₹50,000 per transaction
- Mini statement: last 10 transactions with running balance
- Card locks after 3 wrong PINs; unlock it from the admin panel
- Auto sign-out after 3 minutes of inactivity
- Works on phones: the soft-key layout collapses into stacked buttons

Limits and timeouts live at the bottom of `atm_project/settings.py`.

## Admin panel

```bash
python manage.py createsuperuser
```

Then open http://127.0.0.1:8000/admin/ to add accounts (you set a 4-digit PIN in the form),
unlock locked cards, and view the transaction ledger (read-only).

## Run the tests

```bash
python manage.py test
```

## Project layout

```
manage.py
atm_project/            settings, root urls
atm/
  models.py             Account (card, hashed PIN, balance, lock state) and Transaction
  services.py           deposit() / withdraw(), atomic with row locking
  views.py              login, menu, balance, withdraw, deposit, statement, logout
  forms.py              input validation (card, PIN, amounts and limits)
  admin.py              admin setup with PIN field and "unlock" action
  templatetags/         `inr` filter for rupee formatting
  management/commands/  seed_demo
  templates/atm/        pages
  static/atm/style.css  styling
  tests.py              21 tests
```

## Before putting this on a real server

This is a learning/demo project, not real banking software. If you deploy it anywhere public, set
`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` and `DJANGO_ALLOWED_HOSTS` as environment variables,
and serve it over HTTPS.
