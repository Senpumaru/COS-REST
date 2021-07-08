from django.contrib import admin
from .models import CaseArchive, Approval, Case, Comment, Delivery

# Register your models here.
admin.site.register(CaseArchive)
admin.site.register(Case)
admin.site.register(Comment)
admin.site.register(Approval)
admin.site.register(Delivery)
