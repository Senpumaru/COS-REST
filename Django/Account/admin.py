from django.contrib import admin
from .models import ST1010_Permission, ServiceUser

# Register your models here.
admin.site.register(ServiceUser)
admin.site.register(ST1010_Permission)
