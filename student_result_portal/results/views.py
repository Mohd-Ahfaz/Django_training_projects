from django.contrib import messages
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import StudentForm, SubjectForm, ResultForm
from .models import Student, Subject, Result, grade_for_percentage

def dashboard(request):
    context = {
        "student_count": Student.objects.count(),
        "subject_count": Subject.objects.count(),
        "result_count": Result.objects.count(),
        "passed_count": sum(1 for r in Result.objects.select_related("subject") if r.passed),
        "recent_students": Student.objects.order_by("-created_at")[:5],
    }
    return render(request, "results/dashboard.html", context)

def student_list(request):
    q = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if q:
        students = students.filter(Q(full_name__icontains=q) | Q(roll_number__icontains=q) | Q(course__icontains=q))
    return render(request, "results/student_list.html", {"students": students, "q": q})

def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        student = form.save()
        messages.success(request, "Student added successfully.")
        return redirect("student_detail", pk=student.pk)
    return render(request, "results/form.html", {"form": form, "page_title": "Add student"})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student details updated.")
        return redirect("student_detail", pk=student.pk)
    return render(request, "results/form.html", {"form": form, "page_title": "Edit student"})

@require_POST
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student deleted.")
    return redirect("student_list")

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    results = list(student.results.select_related("subject").all())
    total_obtained = sum(float(r.marks_obtained) for r in results)
    total_max = sum(r.subject.max_marks for r in results)
    percentage = (total_obtained / total_max * 100) if total_max else 0
    passed = bool(results) and all(r.passed for r in results)
    context = {
        "student": student, "results": results,
        "total_obtained": total_obtained, "total_max": total_max,
        "percentage": percentage,
        "grade": grade_for_percentage(percentage),
        "overall_status": "PASS" if passed else ("FAIL" if results else "NOT AVAILABLE"),
    }
    return render(request, "results/student_detail.html", context)

def subject_list(request):
    return render(request, "results/subject_list.html", {"subjects": Subject.objects.all()})

def subject_create(request):
    form = SubjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Subject added successfully.")
        return redirect("subject_list")
    return render(request, "results/form.html", {"form": form, "page_title": "Add subject"})

@require_POST
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, "Subject and its associated results deleted.")
    return redirect("subject_list")

def result_create(request):
    form = ResultForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        result = form.save(commit=False)
        try:
            result.full_clean()
            result.save()
            messages.success(request, "Result saved successfully.")
            return redirect("student_detail", pk=result.student_id)
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(request, "results/form.html", {"form": form, "page_title": "Enter result"})
