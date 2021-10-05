from .models import Patient, Block, BlockGroup, Slide, SlideGroup
from django.contrib import admin

# Register your models here.
admin.site.register(Patient)
admin.site.register(Block)
admin.site.register(BlockGroup)
admin.site.register(Slide)
admin.site.register(SlideGroup)