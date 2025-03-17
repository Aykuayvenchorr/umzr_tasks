from django.urls import path
import app_econ.views


urlpatterns = [
    path('project/<int:id>/', app_econ.views.project, name='project'),
    path('project/<int:id>/save/', app_econ.views.save_project, name='save_project'),
]