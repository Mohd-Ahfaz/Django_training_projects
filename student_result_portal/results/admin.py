from django.contrib import admin
from .models import Student, Subject, Result

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "full_name", "course", "semester", "academic_year")
    search_fields = ("roll_number", "full_name", "email")
    list_filter = ("course", "semester", "academic_year")

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "max_marks", "pass_marks")
    search_fields = ("code", "name")

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "marks_obtained", "exam_name", "updated_at")
    list_filter = ("exam_name", "subject")
    search_fields = ("student__roll_number", "student__full_name", "subject__name")
