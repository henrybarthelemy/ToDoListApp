from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import CreateUserForm

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
