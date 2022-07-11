from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewLoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    return render(request, 'web_app/index.html')


def login_user(request):
    if request.method == "GET":
        return render(request, 'web_app/login.html', {
            'form': NewLoginForm()
        })
    elif request.method == "POST":
        form = NewLoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(
                request, username=form.cleaned_data['username'], password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))


def profile(request):
    return render(request, ('web_app/profile.html'))
