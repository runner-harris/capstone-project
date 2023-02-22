from django.contrib import admin
from .models import Scan

# Register your models here.
# this file makes database models visible on the admin page

# the line of code below makes the scan display show all of the attributes on the screen (aka more readable)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("scanName", "description", "target", "schedule", "date",)

admin.site.register(Scan, ScanAdmin)
