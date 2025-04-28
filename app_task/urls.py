from django.urls import path, re_path
import app_task.views


urlpatterns = [
    re_path(r'^add/(?P<type>[^/]+)/(?P<id>[0-9]+)/(?P<tid>-?[0-9]+)/$', app_task.views.task_add, name='task_add'),
    # path('add/<str:type>/<int:id>/<int:tid>/', app_task.views.task_add, name='task_add'),
]