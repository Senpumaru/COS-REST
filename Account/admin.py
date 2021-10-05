from django.contrib import admin
from .models import ST1010_Permission, ST1011_Permission, ServiceUser

# Register your models here.
admin.site.register(ServiceUser)
admin.site.register(ST1010_Permission)
admin.site.register(ST1011_Permission)
