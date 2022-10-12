from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import SecurityList, SecurityEditCreate, save_security

app_name = 'security'

urlpatterns = [
                  path('', SecurityList.as_view(), name='securitylist'),
                  path('edit', SecurityEditCreate.as_view(), name='security_edit_create'),
                  path('ajax_save_security', save_security, name='ajax_save_security'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
