from django.contrib import admin

from app_econ.models import *

admin.site.register(Project)
admin.site.register(BusinessPlan)
admin.site.register(PaymentBPTask)
admin.site.register(BPTask)
admin.site.register(BusinessPlanStr)
admin.site.register(BusinessPlanFacility)
admin.site.register(BusinessPlanCostItem)
admin.site.register(ProjectStage)