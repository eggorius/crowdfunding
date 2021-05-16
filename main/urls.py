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
    path('company/<int:pk>/update', views.update_company, name='update-company'),
    path('company/new/', views.create_company, name='create-company'),
    path('add-rating/', views.add_star_rating, name='add-rating'),
    path('upload-company-images/<int:pk>', views.upload_company_images, name='company-images'),
    path('company/<int:pk>/delete', views.delete_company, name='delete-company'),
    path('company/<int:pk>/comments/new', views.leave_comment, name='create-comment'),
    path('search', views.search_view, name='search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
