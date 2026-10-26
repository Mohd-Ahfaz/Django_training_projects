from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import TaskForm
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    if query:
        tasks = tasks.filter(title__icontains=query) | tasks.filter(description__icontains=query)
    if status == "pending":
        tasks = tasks.filter(is_completed=False)
    elif status == "completed":
        tasks = tasks.filter(is_completed=True)

    context = {
        "tasks": tasks.distinct(),
        "query": query,
        "status": status,
        "total_count": Task.objects.count(),
        "completed_count": Task.objects.filter(is_completed=True).count(),
        "pending_count": Task.objects.filter(is_completed=False).count(),
    }
    return render(request, "tasks/task_list.html", context)

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully.")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Add a task"})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Edit task"})

@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save(update_fields=["is_completed"])
    return redirect("task_list")

@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("task_list")
