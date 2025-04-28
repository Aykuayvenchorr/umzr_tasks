from django.contrib import admin

from app_task.models import *

admin.site.register(Task)
admin.site.register(PlanCost)
admin.site.register(PlanDateStart)
admin.site.register(PlanDateEnd)
