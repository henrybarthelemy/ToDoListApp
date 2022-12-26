from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskCreateForm

# Create your views here.


def task_create_view(request):
    if request.user.is_authenticated:
        form = TaskCreateForm(request.POST or None)
        if request.method == "POST":
            new_task = form.save()
            new_task.created_by = request.user
            new_task.save()
            form = TaskCreateForm()
        return render(request, "tasks/create_task.html", {"form": form})
    else:
        return redirect("login")


def task_detail_view(request):
    if request.user.is_authenticated:
        objs = Task.objects.filter(created_by=request.user)
        return render(request, "tasks/home.html", {"objects": objs})
    else:
        return redirect("login")


def update_task_view(request, id):
    obj = get_object_or_404(Task, id=id)

    if request.method == "POST":
        if 'finish' in request.POST:
            obj.finished = True
            obj.save()
            return redirect("/" + str(obj.id))
        elif 'unfinish' in request.POST:
            obj.finished = False
            obj.save()
            return redirect("/" + str(obj.id))
        else:
            obj.delete()
            return redirect("/")
    return render(request, "tasks/update_task.html", {"object": obj})
