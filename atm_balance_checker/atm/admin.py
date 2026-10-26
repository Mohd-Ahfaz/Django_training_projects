from django import forms
from django.contrib import admin

from .models import Account, Transaction


class AccountAdminForm(forms.ModelForm):
    new_pin = forms.RegexField(
        regex=r"^\d{4}$",
        required=False,
        label="PIN",
        help_text="4 digits. Leave blank to keep the current PIN.",
        widget=forms.PasswordInput(render_value=False),
        error_messages={"invalid": "PIN must be exactly 4 digits."},
    )

    class Meta:
        model = Account
        fields = ["card_number", "holder_name", "balance", "is_locked", "failed_attempts"]

    def clean(self):
        cleaned = super().clean()
        if not self.instance.pk and not cleaned.get("new_pin"):
            self.add_error("new_pin", "Set a 4-digit PIN for the new account.")
        return cleaned


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = ("holder_name", "masked_card", "balance", "is_locked", "failed_attempts")
    list_filter = ("is_locked",)
    search_fields = ("holder_name", "card_number")
    actions = ["unlock_accounts"]

    def save_model(self, request, obj, form, change):
        pin = form.cleaned_data.get("new_pin")
        if pin:
            obj.set_pin(pin)
        super().save_model(request, obj, form, change)

    @admin.action(description="Unlock selected cards")
    def unlock_accounts(self, request, queryset):
        count = queryset.update(is_locked=False, failed_attempts=0)
        self.message_user(request, f"{count} card(s) unlocked.")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "account", "kind", "amount", "balance_after")
    list_filter = ("kind",)
    # The ledger is a record of what happened: read-only in the admin
    readonly_fields = ("account", "kind", "amount", "balance_after", "created_at")

    def has_add_permission(self, request):
        return False
