from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import EmployeeForm, SalarySlipForm
from .models import Employee, SalarySlip

def dashboard(request):
    slips = SalarySlip.objects.select_related("employee")
    total_net = sum((s.net_salary for s in slips), start=0)
    context = {
        "employee_count": Employee.objects.count(),
        "slip_count": SalarySlip.objects.count(),
        "total_net": total_net,
        "recent_slips": slips[:6],
    }
    return render(request, "payroll/dashboard.html", context)

def employee_list(request):
    q = request.GET.get("q", "").strip()
    employees = Employee.objects.all()
    if q:
        employees = employees.filter(
            Q(full_name__icontains=q) | Q(employee_id__icontains=q) |
            Q(department__icontains=q) | Q(designation__icontains=q)
        )
    return render(request, "payroll/employee_list.html", {"employees": employees, "q": q})

def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        employee = form.save()
        messages.success(request, "Employee added successfully.")
        return redirect("employee_detail", pk=employee.pk)
    return render(request, "payroll/form.html", {"form": form, "page_title": "Add employee"})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Employee details updated.")
        return redirect("employee_detail", pk=employee.pk)
    return render(request, "payroll/form.html", {"form": form, "page_title": "Edit employee"})

@require_POST
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, "Employee and associated salary slips deleted.")
    return redirect("employee_list")

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    slips = employee.salary_slips.all()
    return render(request, "payroll/employee_detail.html", {"employee": employee, "slips": slips})

def slip_list(request):
    slips = SalarySlip.objects.select_related("employee")
    q = request.GET.get("q", "").strip()
    month = request.GET.get("month", "")
    year = request.GET.get("year", "")
    if q:
        slips = slips.filter(Q(employee__full_name__icontains=q) | Q(employee__employee_id__icontains=q))
    if month.isdigit():
        slips = slips.filter(month=int(month))
    if year.isdigit():
        slips = slips.filter(year=int(year))
    return render(request, "payroll/slip_list.html", {
        "slips": slips, "q": q, "month": month, "year": year,
        "months": SalarySlip._meta.get_field("month").choices,
    })

def slip_create(request):
    form = SalarySlipForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        slip = form.save(commit=False)
        try:
            slip.full_clean()
            slip.save()
            messages.success(request, "Salary slip created successfully.")
            return redirect("slip_detail", pk=slip.pk)
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(request, "payroll/form.html", {"form": form, "page_title": "Create salary slip"})

def slip_detail(request, pk):
    slip = get_object_or_404(SalarySlip.objects.select_related("employee"), pk=pk)
    return render(request, "payroll/slip_detail.html", {"slip": slip})

@require_POST
def slip_delete(request, pk):
    slip = get_object_or_404(SalarySlip, pk=pk)
    slip.delete()
    messages.success(request, "Salary slip deleted.")
    return redirect("slip_list")
