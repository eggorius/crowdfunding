from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from braces.views import LoginRequiredMixin
from .models import *


@login_required(login_url='login/')
def my_companies_view(request):
    companies = request.user.company_set.all()
    return render(request, 'main/company_list.html', {'companies': companies})


class CompanyDetailView(DetailView):
    model = Company


class CompanyCreateView(CreateView):
    model = Company
    fields = ['title', 'description', 'video_url', 'theme', 'goal', 'date_finish']


def home(request):
    return render(request, 'main/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Your successfully logged in!')
                return redirect('home')
        return render(request, 'main/login.html', {'form': form})
    form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            messages.success(request, f'Your account has been created!')
            return redirect('home')
        return render(request, 'main/register.html', {'form': form})
    form = RegistrationForm(request.POST or None)
    return render(request, 'main/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    return render(request, 'main/profile.html')


