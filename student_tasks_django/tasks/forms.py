from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Complete DBMS assignment"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Add task details (optional)"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
