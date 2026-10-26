import decimal
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("roll_number", models.CharField(max_length=30, unique=True)),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("course", models.CharField(default="B.Tech CSE", max_length=100)),
                ("semester", models.PositiveSmallIntegerField(default=1)),
                ("academic_year", models.CharField(default="2026-27", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["roll_number"]},
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=120)),
                ("max_marks", models.PositiveSmallIntegerField(default=100, validators=[django.core.validators.MinValueValidator(1)])),
                ("pass_marks", models.PositiveSmallIntegerField(default=40, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={"ordering": ["code"]},
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("marks_obtained", models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("exam_name", models.CharField(default="Semester Examination", max_length=100)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="results", to="results.student")),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="results", to="results.subject")),
            ],
            options={"ordering": ["subject__code"], "constraints": [models.UniqueConstraint(fields=("student", "subject", "exam_name"), name="unique_student_subject_exam")]},
        ),
    ]
