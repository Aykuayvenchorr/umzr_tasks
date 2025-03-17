from django.contrib import admin
from app_struct.models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", )
    # list_display = ("id", "name")


# admin.site.register(Company)
admin.site.register(Division)
admin.site.register(Employee)
admin.site.register(License)
admin.site.register(Facility)
admin.site.register(FacilityType)

