from decimal import Decimal

from django.core.management.base import BaseCommand

from atm.models import Account

DEMO_ACCOUNTS = [
    ("4111111111111111", "Aarav Sharma", "1234", Decimal("25000.00")),
    ("5500000000000004", "Priya Verma", "4321", Decimal("120500.50")),
    ("6011000000000004", "Rohan Singh", "2580", Decimal("500.00")),
]


class Command(BaseCommand):
    help = "Create (or reset) demo accounts so you can try the ATM straight away."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Demo accounts ready:\n"))
        for card, name, pin, balance in DEMO_ACCOUNTS:
            account, _ = Account.objects.get_or_create(
                card_number=card, defaults={"holder_name": name}
            )
            account.holder_name = name
            account.balance = balance
            account.is_locked = False
            account.failed_attempts = 0
            account.set_pin(pin)
            account.save()
            self.stdout.write(f"  {name:<14} card {card}   PIN {pin}")
        self.stdout.write("")
