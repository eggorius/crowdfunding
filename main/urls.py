from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('mycompanies/', views.my_companies_view, name='my-companies'),
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company'),
    path('company/new/', views.CompanyCreateView.as_view(), name='company-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)