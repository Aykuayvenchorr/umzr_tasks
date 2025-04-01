from django.urls import path
import app_comments.views


urlpatterns = [
    path('<int:id>/', app_comments.views.comment_unchecked, name='comment_unchecked'),
    path('save/', app_comments.views.comment_save, name='comment_save'),
    # path('<str:type>/<int:id>/<int:id_comment>/', app_comments.views.comment_onchecked, name='comment_onchecked'),
]