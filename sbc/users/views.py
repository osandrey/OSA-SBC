from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms


@login_required
def logout_user(request):
    logout(request)
    return redirect(to='users:main')

# Create your views here.
def main(request):
    return render(request=request, template_name='users/index.html', context={})

def create_user_profile(request):
    if request.user.is_authenticated:
        return redirect('users:main')

    if request.method == 'POST':
        form = forms.CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login_user')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    form = forms.CustomUserRegisterForm()
    return render(request, 'users/signup.html', context={"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(to='users:main')


    if request.method == 'POST':
        print('I\'m in POST')
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print('I\'m in POST but user is NONE ')
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:main')

        login(request, user)
        return redirect(to='users:main')

    form = forms.LoginForm()
    return render(request, 'users/login.html', context={"form": form})



