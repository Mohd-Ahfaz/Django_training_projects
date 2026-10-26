from decimal import Decimal

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Account(models.Model):
    """A bank account that can be accessed with a card number + PIN."""

    card_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[RegexValidator(r"^\d{16}$", "Card number must be exactly 16 digits.")],
    )
    holder_name = models.CharField(max_length=100)
    pin_hash = models.CharField(max_length=128, editable=False)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["holder_name"]

    def __str__(self):
        return f"{self.holder_name} ({self.masked_card})"

    # ---- card helpers -------------------------------------------------
    @property
    def masked_card(self):
        return f"**** **** **** {self.card_number[-4:]}"

    # ---- PIN handling (never stored in plain text) ---------------------
    def set_pin(self, raw_pin):
        self.pin_hash = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin_hash)

    def register_failed_attempt(self):
        """Count a wrong PIN and lock the card once the limit is reached."""
        self.failed_attempts += 1
        if self.failed_attempts >= settings.ATM_MAX_PIN_ATTEMPTS:
            self.is_locked = True
        self.save(update_fields=["failed_attempts", "is_locked"])

    def reset_failed_attempts(self):
        if self.failed_attempts:
            self.failed_attempts = 0
            self.save(update_fields=["failed_attempts"])


class Transaction(models.Model):
    DEPOSIT = "DEP"
    WITHDRAWAL = "WDL"
    KIND_CHOICES = [(DEPOSIT, "Deposit"), (WITHDRAWAL, "Withdrawal")]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    kind = models.CharField(max_length=3, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.get_kind_display()} {self.amount} on {self.created_at:%d %b %Y}"
