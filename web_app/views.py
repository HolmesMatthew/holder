from multiprocessing import context
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#
from . models import Task
from .forms import LoginForm, SignUpForm, TaskForm


# Create your views here.


def index(request):

    return render(request, 'web_app/index.html',)


def sign_up(request):
    if request.method == "GET":
        return render(request, 'web_app/signup.html', {
            'form': SignUpForm()
        })
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            return HttpResponseRedirect(reverse('login_user'))
        else:
            return HttpResponseRedirect(reverse('signup'))


def login_user(request):
    if request.method == "GET":
        return render(request, 'web_app/login.html', {
            'form': LoginForm()
        })
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(
                request, username=form.cleaned_data['username'], password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))
            else:
                form.add_error('username', 'Invalid Credentials')
                return render(request, 'web_app/login.html', {
                    'form': form
                })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_user'))


@login_required
def profile(request):

    context = {
        'tasks': Task.objects.all().filter(user=request.user),
        'form': TaskForm()
    }
    return render(request, 'web_app/profile.html', context)

# ------------------------


def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task()
            task.user = request.user
            task.title = form.cleaned_data['title']
            task.save()
        return HttpResponseRedirect(reverse('profile'))


def edit(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    context = {
        'task': task,
        'form': form
    }
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'web_app/edit.html', context)


def delete_task(request, pk):
    item = Task.objects.get(id=pk)
    item.delete()
    return redirect('profile')
