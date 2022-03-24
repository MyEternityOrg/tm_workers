from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import UserLogin, UserLogout

app_name = 'users'

urlpatterns = [
                  path('', UserLogin.as_view(), name='user_login'),
                  path('', UserLogout.as_view(), name='user_logout'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
