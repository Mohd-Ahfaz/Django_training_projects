import decimal
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(max_length=30, unique=True)),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=25)),
                ("department", models.CharField(max_length=100)),
                ("designation", models.CharField(max_length=100)),
                ("date_joined", models.DateField(blank=True, null=True)),
                ("bank_account_last4", models.CharField(blank=True, max_length=4, verbose_name="Bank account last 4 digits")),
            ],
            options={"ordering": ["employee_id"]},
        ),
        migrations.CreateModel(
            name="SalarySlip",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("month", models.PositiveSmallIntegerField(choices=[(1,"January"),(2,"February"),(3,"March"),(4,"April"),(5,"May"),(6,"June"),(7,"July"),(8,"August"),(9,"September"),(10,"October"),(11,"November"),(12,"December")])),
                ("year", models.PositiveSmallIntegerField()),
                ("basic_salary", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))])),
                ("hra", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))], verbose_name="House rent allowance (HRA)")),
                ("other_allowances", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))])),
                ("bonus", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))])),
                ("pf_deduction", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))], verbose_name="Provident fund deduction")),
                ("tax_deduction", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))], verbose_name="Tax deduction")),
                ("other_deductions", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.00"))])),
                ("payment_date", models.DateField(blank=True, null=True)),
                ("notes", models.CharField(blank=True, max_length=250)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="salary_slips", to="payroll.employee")),
            ],
            options={"ordering": ["-year", "-month", "employee__employee_id"], "constraints": [models.UniqueConstraint(fields=("employee","month","year"), name="unique_employee_salary_month")]},
        ),
    ]
