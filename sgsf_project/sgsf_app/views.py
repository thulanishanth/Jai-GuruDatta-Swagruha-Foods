from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import MenuItem

def index(request):
    return render(request, 'sgsf_app/index.html')

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'sgsf_app/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'sgsf_app/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'sgsf_app/login.html')

@login_required
def home(request):
    return render(request, 'sgsf_app/home.html')

@login_required
def menu(request):
    items = MenuItem.objects.all()
    return render(request, "sgsf_app/menu.html", {"items": items})

def logout_view(request):
    logout(request)
    return redirect('index')
