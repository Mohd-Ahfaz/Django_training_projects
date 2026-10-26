from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

ZERO = Decimal("0.00")

class Employee(models.Model):
    employee_id = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    date_joined = models.DateField(null=True, blank=True)
    bank_account_last4 = models.CharField(max_length=4, blank=True, verbose_name="Bank account last 4 digits")

    class Meta:
        ordering = ["employee_id"]

    def __str__(self):
        return f"{self.employee_id} — {self.full_name}"

class SalarySlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salary_slips")
    month = models.PositiveSmallIntegerField(choices=[(i, name) for i, name in enumerate(
        ["", "January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"]) if i])
    year = models.PositiveSmallIntegerField()
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    hra = models.DecimalField("House rent allowance (HRA)", max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    pf_deduction = models.DecimalField("Provident fund deduction", max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    tax_deduction = models.DecimalField("Tax deduction", max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=ZERO, validators=[MinValueValidator(ZERO)])
    payment_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "-month", "employee__employee_id"]
        constraints = [models.UniqueConstraint(fields=["employee", "month", "year"], name="unique_employee_salary_month")]

    def __str__(self):
        return f"{self.employee.full_name} — {self.get_month_display()} {self.year}"

    @property
    def gross_salary(self):
        return self.basic_salary + self.hra + self.other_allowances + self.bonus

    @property
    def total_deductions(self):
        return self.pf_deduction + self.tax_deduction + self.other_deductions

    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.total_deductions > self.gross_salary:
            raise ValidationError("Total deductions cannot exceed gross salary.")
