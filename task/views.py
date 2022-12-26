from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskCreateForm, CreateUserForm
from django.contrib import auth

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'auth/login.html', context)


def signout_view(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        auth.logout(request)
        return redirect("/")


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        return render(request, "auth/register.html", {"form": form})


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
