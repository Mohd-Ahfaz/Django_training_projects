from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Account, Transaction
from .templatetags.atm_extras import inr

CARD = "4111111111111111"
PIN = "1234"


def make_account(balance="5000.00", card=CARD, pin=PIN):
    account = Account(card_number=card, holder_name="Test User", balance=Decimal(balance))
    account.set_pin(pin)
    account.save()
    return account


class LoginTests(TestCase):
    def setUp(self):
        self.account = make_account()

    def login(self, card=CARD, pin=PIN):
        return self.client.post(reverse("atm:login"), {"card_number": card, "pin": pin})

    def test_login_success_redirects_to_menu(self):
        response = self.login()
        self.assertRedirects(response, reverse("atm:menu"))

    def test_card_number_with_spaces_is_accepted(self):
        response = self.login(card="4111 1111 1111 1111")
        self.assertRedirects(response, reverse("atm:menu"))

    def test_wrong_pin_is_rejected_and_counted(self):
        response = self.login(pin="9999")
        self.assertContains(response, "Card number or PIN is incorrect.")
        self.account.refresh_from_db()
        self.assertEqual(self.account.failed_attempts, 1)

    def test_unknown_card_gets_same_message(self):
        response = self.login(card="1234567812345678")
        self.assertContains(response, "Card number or PIN is incorrect.")

    def test_card_locks_after_three_wrong_pins(self):
        for _ in range(3):
            self.login(pin="0000")
        self.account.refresh_from_db()
        self.assertTrue(self.account.is_locked)
        # even the right PIN is refused now
        response = self.login()
        self.assertContains(response, "locked")

    def test_successful_login_resets_failed_attempts(self):
        self.login(pin="0000")
        self.login()
        self.account.refresh_from_db()
        self.assertEqual(self.account.failed_attempts, 0)

    def test_pin_is_stored_hashed(self):
        self.assertNotEqual(self.account.pin_hash, PIN)
        self.assertTrue(self.account.check_pin(PIN))

    def test_logout_clears_session(self):
        self.login()
        self.client.post(reverse("atm:logout"))
        response = self.client.get(reverse("atm:menu"))
        self.assertRedirects(response, reverse("atm:login"))


class ProtectedPageTests(TestCase):
    def test_pages_require_login(self):
        for name in ["menu", "balance", "withdraw", "deposit", "statement"]:
            response = self.client.get(reverse(f"atm:{name}"))
            self.assertRedirects(response, reverse("atm:login"), msg_prefix=name)

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get(reverse("atm:logout")).status_code, 405)


class TransactionTests(TestCase):
    def setUp(self):
        self.account = make_account()
        self.client.post(reverse("atm:login"), {"card_number": CARD, "pin": PIN})

    def test_balance_page_shows_balance(self):
        response = self.client.get(reverse("atm:balance"))
        self.assertContains(response, "₹5,000.00")

    def test_withdraw_reduces_balance_and_logs_it(self):
        response = self.client.post(reverse("atm:withdraw"), {"amount": "1500"})
        self.assertRedirects(response, reverse("atm:balance"))
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("3500.00"))
        txn = Transaction.objects.get()
        self.assertEqual(txn.kind, Transaction.WITHDRAWAL)
        self.assertEqual(txn.balance_after, Decimal("3500.00"))

    def test_withdraw_more_than_balance_is_refused(self):
        response = self.client.post(reverse("atm:withdraw"), {"amount": "6000"})
        self.assertContains(response, "balance is too low")
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("5000.00"))
        self.assertEqual(Transaction.objects.count(), 0)

    def test_withdraw_must_be_multiple_of_100(self):
        response = self.client.post(reverse("atm:withdraw"), {"amount": "450"})
        self.assertContains(response, "multiples of")
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("5000.00"))

    def test_withdraw_limit_per_transaction(self):
        self.account.balance = Decimal("100000")
        self.account.save()
        response = self.client.post(reverse("atm:withdraw"), {"amount": "25000"})
        self.assertContains(response, "limit")

    def test_negative_and_zero_amounts_are_refused(self):
        for bad in ["-100", "0", "abc", ""]:
            self.client.post(reverse("atm:withdraw"), {"amount": bad})
            self.client.post(reverse("atm:deposit"), {"amount": bad})
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("5000.00"))
        self.assertEqual(Transaction.objects.count(), 0)

    def test_deposit_increases_balance(self):
        self.client.post(reverse("atm:deposit"), {"amount": "250.50"})
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("5250.50"))

    def test_statement_lists_transactions_newest_first(self):
        self.client.post(reverse("atm:deposit"), {"amount": "100"})
        self.client.post(reverse("atm:withdraw"), {"amount": "200"})
        response = self.client.get(reverse("atm:statement"))
        kinds = [t.kind for t in response.context["transactions"]]
        self.assertEqual(kinds, [Transaction.WITHDRAWAL, Transaction.DEPOSIT])

    def test_empty_statement_message(self):
        response = self.client.get(reverse("atm:statement"))
        self.assertContains(response, "No transactions yet")

    def test_users_only_see_their_own_data(self):
        other = make_account(balance="999.00", card="5500000000000004", pin="4321")
        Transaction.objects.create(
            account=other, kind=Transaction.DEPOSIT, amount=1, balance_after=999
        )
        response = self.client.get(reverse("atm:statement"))
        self.assertEqual(len(response.context["transactions"]), 0)


class FormatTests(TestCase):
    def test_indian_grouping(self):
        self.assertEqual(inr(Decimal("0")), "₹0.00")
        self.assertEqual(inr(Decimal("999.5")), "₹999.50")
        self.assertEqual(inr(Decimal("1000")), "₹1,000.00")
        self.assertEqual(inr(Decimal("120500.5")), "₹1,20,500.50")
        self.assertEqual(inr(Decimal("12345678.9")), "₹1,23,45,678.90")
