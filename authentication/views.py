from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout as lgout, login as lgin
from .forms import UserRegisterForm, UserLoginForm

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/dash/agent/')

    elif request.method == 'GET':
        form = UserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


def login(request):

    if request.method == 'POST':

        form = UserLoginForm(request.POST)
        User = authenticate(username=request.POST['username'], password=request.POST['password'])

        if User.userrole.supervisor and User.is_authenticated:
            messages.success(request, f'Login Successful! Redirecting..')
            lgin(request, User)
            return redirect('/dash/department/', request=request)

        elif User.userrole.agent and User.is_authenticated:
            lgin(request, User)
            messages.success(request, f'Login Successful! Redirecting..')
            return redirect('/dash/agent/')

        else:
            return HttpResponse("Invalid Credentials!")

    elif request.method == 'GET':

        form = UserLoginForm()
        return render(request, 'authentication/login.html', {'form':form})


def logout(request):
    lgout(request)
    form = UserLoginForm()
    return redirect('/login')