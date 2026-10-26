from django.contrib import admin
from .models import Employee, SalarySlip

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "department", "designation", "email")
    search_fields = ("employee_id", "full_name", "department")
    list_filter = ("department",)

@admin.register(SalarySlip)
class SalarySlipAdmin(admin.ModelAdmin):
    list_display = ("employee", "month", "year", "basic_salary", "gross_salary_display", "net_salary_display")
    list_filter = ("month", "year")
    search_fields = ("employee__employee_id", "employee__full_name")

    @admin.display(description="Gross salary")
    def gross_salary_display(self, obj):
        return obj.gross_salary

    @admin.display(description="Net salary")
    def net_salary_display(self, obj):
        return obj.net_salary
