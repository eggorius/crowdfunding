from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
from .models import *
from .decorators import check_for_authority
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator
import json


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
            tags_title = request.POST.get('tags-input')
            form.instance.author_id = request.user.id
            form.save()
            if len(tags_title):
                tags_parsed = parse_tagify_tags(tags_title)
                for tag in tags_parsed:
                    t = Tag(title=tag)
                    if not Tag.objects.filter(title=tag).exists():
                        t.save()
                        form.instance.tags.add(t)
                    else:
                        form.instance.tags.add(Tag.objects.filter(title=t).first())
            return redirect('my-companies')
    form = CompanyForm(request.POST or None)
    return render(request, 'main/company_create_form.html', {'form': form})


def parse_tagify_tags(tags_titles):
    tags_titles = json.loads(tags_titles)
    tags_titles_parsed = [t["value"] for t in tags_titles]
    return tags_titles_parsed


def home(request):
    companies = Company.objects.all()
    all_tags = Tag.objects.all()
    data = serializers.serialize('json', list(all_tags), fields='title')
    if request.method == 'POST':
        tag_titles = request.POST.get('tags-jquery')
        if len(tag_titles):
            tags_parsed = parse_tagify_tags(tag_titles)
            tags = Tag.objects.filter(title__in=tags_parsed)
            companies = set(Company.objects.filter(tags__in=tags))
            return render(request, 'main/home.html', {'companies': companies, 'tags': all_tags,
                                                      'data': data})
    paginator = Paginator(companies, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'tags': all_tags,
                                              'data': data, 'companies': page_obj})


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
        print('I worked')
        if form.is_valid():
            Rating.objects.update_or_create(
                author_id=request.user.id,
                company_id=int(request.POST.get('company')),
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
        return HttpResponse(200)


def search_view(request):
    if request.method == 'POST':
        q = request.POST['search']
        results = Company.objects.annotate(
            search=SearchVector('title', 'description', 'comments__content')
        ).filter(search=SearchQuery(q, search_type='raw'))
        return render(request, 'main/search_results.html', {'q': q, 'results': results})

    return render(request, 'main/search_results.html')
