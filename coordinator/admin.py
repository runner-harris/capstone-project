from django.contrib import admin
from .models import Scan

# Register your models here.
class ScanAdmin(admin.ModelAdmin):
    list_display = ("scanName", "description", "target",)

admin.site.register(Scan, ScanAdmin)
