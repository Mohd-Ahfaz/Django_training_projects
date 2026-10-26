from django import forms
from .models import Employee, SalarySlip

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["employee_id", "full_name", "email", "phone", "department", "designation", "date_joined", "bank_account_last4"]
        widgets = {"date_joined": forms.DateInput(attrs={"type": "date"})}

class SalarySlipForm(forms.ModelForm):
    class Meta:
        model = SalarySlip
        fields = [
            "employee", "month", "year", "basic_salary", "hra", "other_allowances",
            "bonus", "pf_deduction", "tax_deduction", "other_deductions",
            "payment_date", "notes"
        ]
        widgets = {"payment_date": forms.DateInput(attrs={"type": "date"})}
