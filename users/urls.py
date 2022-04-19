from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import UserLogin, UserLogout, UserMain

app_name = 'users'

urlpatterns = [
                  path('', UserLogin.as_view(), name='login'),
                  path('accounts/login/', UserLogin.as_view(), name='login'),
                  path('logout/', UserLogout.as_view(), name='logout'),
                  path('index/', UserMain.as_view(), name='index'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
