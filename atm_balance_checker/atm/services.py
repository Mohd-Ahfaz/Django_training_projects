"""Money-moving logic lives here so views stay thin and tests are easy."""
from decimal import Decimal

from django.db import transaction

from .models import Account, Transaction


class InsufficientFunds(Exception):
    pass


@transaction.atomic
def deposit(account_id, amount: Decimal) -> Account:
    # select_for_update locks the row so two requests can't race each other
    account = Account.objects.select_for_update().get(pk=account_id)
    account.balance += amount
    account.save(update_fields=["balance"])
    Transaction.objects.create(
        account=account,
        kind=Transaction.DEPOSIT,
        amount=amount,
        balance_after=account.balance,
    )
    return account


@transaction.atomic
def withdraw(account_id, amount: Decimal) -> Account:
    account = Account.objects.select_for_update().get(pk=account_id)
    if amount > account.balance:
        raise InsufficientFunds
    account.balance -= amount
    account.save(update_fields=["balance"])
    Transaction.objects.create(
        account=account,
        kind=Transaction.WITHDRAWAL,
        amount=amount,
        balance_after=account.balance,
    )
    return account
