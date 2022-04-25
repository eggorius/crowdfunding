from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls'))
]

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
)
