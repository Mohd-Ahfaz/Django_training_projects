from decimal import Decimal

from django import forms
from django.conf import settings


class LoginForm(forms.Form):
    card_number = forms.RegexField(
        regex=r"^\d{16}$",
        label="Card number",
        error_messages={"invalid": "Enter the 16 digits of your card number."},
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "autocomplete": "off",
                "maxlength": "16",
                "placeholder": "16-digit card number",
            }
        ),
    )
    pin = forms.RegexField(
        regex=r"^\d{4}$",
        label="PIN",
        error_messages={"invalid": "Your PIN is 4 digits."},
        widget=forms.PasswordInput(
            attrs={
                "inputmode": "numeric",
                "autocomplete": "off",
                "maxlength": "4",
                "placeholder": "4-digit PIN",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Let people paste numbers with spaces/dashes: keep digits only
        if self.is_bound:
            data = self.data.copy()
            raw = data.get("card_number", "")
            data["card_number"] = "".join(ch for ch in raw if ch.isdigit())
            self.data = data


class AmountForm(forms.Form):
    amount = forms.DecimalField(
        min_value=Decimal("1"),
        max_digits=10,
        decimal_places=2,
        label="Amount (₹)",
        widget=forms.NumberInput(attrs={"inputmode": "decimal", "placeholder": "0", "step": "any"}),
    )
    max_amount = None
    multiple_of = None

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if self.max_amount is not None and amount > self.max_amount:
            raise forms.ValidationError(
                f"The limit is ₹{self.max_amount:,} per transaction."
            )
        if self.multiple_of and amount % self.multiple_of != 0:
            raise forms.ValidationError(
                f"Enter an amount in multiples of ₹{self.multiple_of}."
            )
        return amount


class WithdrawForm(AmountForm):
    max_amount = settings.ATM_MAX_WITHDRAWAL
    multiple_of = settings.ATM_NOTE_MULTIPLE


class DepositForm(AmountForm):
    max_amount = settings.ATM_MAX_DEPOSIT
