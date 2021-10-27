from django.urls import path

from .views import UserLogin, ajax_login_user

app_name = 'users'

urlpatterns = [
    path('', UserLogin.as_view(), name='user_login'),
    path('ajax_login_user/', ajax_login_user, name='dynamic_login'),
]
