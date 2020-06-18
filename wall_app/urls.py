from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('success', views.success),
    path('login', views.login),
    path('create_message', views.create_message),
    path('post_comment/<int:mess_id>', views.post_comment),
    path('log_out', views.log_out),
]