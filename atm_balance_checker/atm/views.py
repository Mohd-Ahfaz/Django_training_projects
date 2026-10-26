from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import DepositForm, LoginForm, WithdrawForm
from .models import Account

SESSION_KEY = "atm_account_id"


def atm_login_required(view):
    """Only let through people who have entered a valid card + PIN."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        account_id = request.session.get(SESSION_KEY)
        if not account_id:
            return redirect("atm:login")
        try:
            request.account = Account.objects.get(pk=account_id, is_locked=False)
        except Account.DoesNotExist:
            request.session.flush()
            return redirect("atm:login")
        return view(request, *args, **kwargs)

    return wrapper


def login_view(request):
    if request.session.get(SESSION_KEY):
        return redirect("atm:menu")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        card = form.cleaned_data["card_number"]
        pin = form.cleaned_data["pin"]
        account = Account.objects.filter(card_number=card).first()

        if account and account.is_locked:
            messages.error(
                request,
                "This card is locked after too many wrong PINs. Please contact your bank.",
            )
        elif account and account.check_pin(pin):
            account.reset_failed_attempts()
            request.session.cycle_key()  # new session id on login
            request.session[SESSION_KEY] = account.pk
            return redirect("atm:menu")
        else:
            if account:
                account.register_failed_attempt()
                if account.is_locked:
                    messages.error(
                        request,
                        "Wrong PIN again. This card is now locked. Please contact your bank.",
                    )
                    return render(request, "atm/login.html", {"form": LoginForm()})
            # Same message for unknown card and wrong PIN, so nobody can probe card numbers
            messages.error(request, "Card number or PIN is incorrect.")
    return render(request, "atm/login.html", {"form": form})


@require_POST
def logout_view(request):
    request.session.flush()
    messages.success(request, "You're signed out. Don't forget your card.")
    return redirect("atm:login")


@atm_login_required
def menu_view(request):
    return render(request, "atm/menu.html", {"account": request.account})


@atm_login_required
def balance_view(request):
    return render(request, "atm/balance.html", {"account": request.account})


@atm_login_required
def statement_view(request):
    rows = request.account.transactions.all()[: settings.ATM_STATEMENT_LENGTH]
    return render(
        request,
        "atm/statement.html",
        {"account": request.account, "transactions": rows},
    )


@atm_login_required
def withdraw_view(request):
    form = WithdrawForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        try:
            services.withdraw(request.account.pk, amount)
        except services.InsufficientFunds:
            form.add_error("amount", "Your balance is too low for this withdrawal.")
        else:
            messages.success(request, f"Please collect your cash: ₹{amount:,.2f}")
            return redirect("atm:balance")
    return render(
        request,
        "atm/amount_form.html",
        {
            "account": request.account,
            "form": form,
            "title": "Withdraw cash",
            "hint": f"Multiples of ₹{settings.ATM_NOTE_MULTIPLE}, up to ₹{settings.ATM_MAX_WITHDRAWAL:,} per transaction.",
            "button": "Withdraw",
            "quick_amounts": [500, 1000, 2000, 5000],
        },
    )


@atm_login_required
def deposit_view(request):
    form = DepositForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        services.deposit(request.account.pk, amount)
        messages.success(request, f"₹{amount:,.2f} added to your account.")
        return redirect("atm:balance")
    return render(
        request,
        "atm/amount_form.html",
        {
            "account": request.account,
            "form": form,
            "title": "Deposit cash",
            "hint": f"Up to ₹{settings.ATM_MAX_DEPOSIT:,} per transaction.",
            "button": "Deposit",
            "quick_amounts": [500, 1000, 5000, 10000],
        },
    )
