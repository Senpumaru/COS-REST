from django.contrib import admin
from .models import Approval, Case, Comment, Delivery

# Register your models here.
admin.site.register(Case)
admin.site.register(Comment)
admin.site.register(Approval)
admin.site.register(Delivery)
