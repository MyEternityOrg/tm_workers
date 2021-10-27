from django.urls import path

from .views import UserLogin

app_name = 'users'

urlpatterns = [
    path('', UserLogin.as_view(), name='user_login'),
]
