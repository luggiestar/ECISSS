from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error('invalid username or password')
            return redirect('login')
    return render(request, 'authentication/user-login.html')


def user_logout(request):
    logout(request)
    return redirect('login_view')