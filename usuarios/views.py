from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Debug: ver qué está llegando
        print(f"[DEBUG] Login attempt - Username: {username}")
        print(f"[DEBUG] Request method: {request.method}")
        print(f"[DEBUG] Request origin: {request.headers.get('origin', 'No origin')}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"[DEBUG] Login successful for user: {username}")
            return redirect("dashboard")
        else:
            print(f"[DEBUG] Login failed for user: {username}")
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "usuarios/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "usuarios/dashboard.html")

