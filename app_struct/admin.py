from django.contrib import admin
from app_struct.models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", )
    # list_display = ("id", "name")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "surname", )

admin.site.register(Division)
admin.site.register(License)
admin.site.register(Facility)
admin.site.register(FacilityType)

