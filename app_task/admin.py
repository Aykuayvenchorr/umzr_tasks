from django.contrib import admin

from app_task.models import *

admin.site.register(Task)
admin.site.register(TermPlanTask)
admin.site.register(PaymentTaskPlan)
