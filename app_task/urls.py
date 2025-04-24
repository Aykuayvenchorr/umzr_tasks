from django.urls import path
import app_task.views


urlpatterns = [
    path('add/<str:type>/<int:id>/<int:tid>/', app_task.views.task_add, name='task_add'),
]