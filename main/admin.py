from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Photo)
admin.site.register(Comment)

# Register your models here.
