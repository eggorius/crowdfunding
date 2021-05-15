from django.http import HttpResponse
from .models import Company


def check_for_authority(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        company = Company.objects.get(id=pk)
        if request.user == company.author or request.user.is_superuser:
            return view_func(request, pk, *args, **kwargs)
        return HttpResponse(status=403)
    return wrapper_func
