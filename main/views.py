from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from .decorators import check_for_authority
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q


@login_required(login_url='login/')
def my_companies_view(request):
    companies = request.user.company_set.all()
    return render(request, 'main/company_list.html', {'companies': companies})


class CompanyDetailView(DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['comment_form'] = CommentForm()
        return context


@login_required
def leave_comment(request, pk):
    company = Company.objects.get(id=pk)
    if request.method == 'POST':
        print('Im here')
        form = CommentForm(request.POST or None)
        if form.is_valid():
            form.instance.author_id = request.user.id
            form.instance.company_id = pk
            form.save()
        return redirect(company.get_absolute_url())


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST or None)
        if form.is_valid():
            form.instance.author_id = request.user.id
            form.save()
            return redirect('my-companies')
    form = CompanyForm(request.POST or None)
    return render(request, 'main/company_create_form.html', {'form': form})


def home(request):
    companies = Company.objects.all()
    return render(request, 'main/home.html', {'companies': companies})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
            user_profile = UserProfile(user_id=new_user.id)
            new_user.save()
            user_profile.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Your account has been created!')
            return redirect('home')
        return render(request, 'main/register.html', {'form': form})
    form = RegistrationForm(request.POST or None)
    return render(request, 'main/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


def add_star_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST or None)
        if form.is_valid():
            Rating.objects.update_or_create(
                author_id=request.user.id,
                company_id=int(request.POST.get('company_id')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


def upload_company_images(request, pk):
    if request.method == 'POST':
        print(request.FILES)
        file = request.FILES.get('file')
        if file is not None:
            Photo.objects.create(
                image=file,
                company_id=pk
            )
        return HttpResponse(201)
    return HttpResponse('')


@login_required
@check_for_authority
def update_company(request, pk):
    company = Company.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect(company.get_absolute_url())
    form = UpdateCompanyForm(instance=company)
    return render(request, 'main/company_update_form.html', {'form': form, 'company': company})


@login_required
@check_for_authority
def delete_company(request, pk):
    if request.method == 'POST':
        company = Company.objects.get(id=pk)
        company.delete()
        print('Everything is working')
        companies = Company.objects.all()
        return render(request, 'main/company_list.html', {'companies': companies})


def get_company_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        companies = Company.objects.filter(
            Q(title__icontains=q) |
            Q(description__in=q)
        ).distinct()
        for company in companies:
            queryset.append(company)
    return list(set(queryset))


def search_view(request):
    if request.method == 'POST':
        q = request.POST['search']
        results = Company.objects.annotate(
            search=SearchVector('title', 'description', 'comments__content')
        ).filter(search=SearchQuery(q, search_type='raw'))
        return render(request, 'main/search_results.html', {'q': q, 'results': results})

    return render(request, 'main/search_results.html')
