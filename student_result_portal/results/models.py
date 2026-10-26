from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Student(models.Model):
    roll_number = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    course = models.CharField(max_length=100, default="B.Tech CSE")
    semester = models.PositiveSmallIntegerField(default=1)
    academic_year = models.CharField(max_length=20, default="2026-27")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["roll_number"]

    def __str__(self):
        return f"{self.roll_number} — {self.full_name}"

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    max_marks = models.PositiveSmallIntegerField(default=100, validators=[MinValueValidator(1)])
    pass_marks = models.PositiveSmallIntegerField(default=40, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.pass_marks > self.max_marks:
            raise ValidationError({"pass_marks": "Pass marks cannot exceed maximum marks."})

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="results")
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    exam_name = models.CharField(max_length=100, default="Semester Examination")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["subject__code"]
        constraints = [models.UniqueConstraint(fields=["student", "subject", "exam_name"], name="unique_student_subject_exam")]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.subject_id and self.marks_obtained is not None:
            subject = self.subject
            if self.marks_obtained > subject.max_marks:
                raise ValidationError({"marks_obtained": f"Marks cannot exceed {subject.max_marks}."})

    @property
    def percentage(self):
        if not self.subject.max_marks:
            return 0
        return float(self.marks_obtained) / self.subject.max_marks * 100

    @property
    def passed(self):
        return self.marks_obtained >= self.subject.pass_marks

def grade_for_percentage(percentage):
    if percentage >= 90: return "A+"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 50: return "D"
    if percentage >= 40: return "E"
    return "F"
