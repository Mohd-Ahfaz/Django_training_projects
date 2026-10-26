import re
from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def inr(value):
    """Format a number as Indian rupees with lakh/crore grouping: 1234567.5 -> ₹12,34,567.50"""
    try:
        amount = Decimal(value).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError, ValueError):
        return value
    sign = "-" if amount < 0 else ""
    whole, frac = f"{abs(amount):.2f}".split(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        head = re.sub(r"(\d+?)(?=(\d\d)+$)", r"\1,", head)
        whole = f"{head},{tail}"
    return f"₹{sign}{whole}.{frac}"
