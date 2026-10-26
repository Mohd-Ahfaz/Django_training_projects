from django import forms
from .models import Student, Subject, Result

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["roll_number", "full_name", "email", "course", "semester", "academic_year"]

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["code", "name", "max_marks", "pass_marks"]

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["student", "subject", "marks_obtained", "exam_name"]
        widgets = {"marks_obtained": forms.NumberInput(attrs={"step": "0.01", "min": "0"})}
