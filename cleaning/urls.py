from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = 'cleaning'

urlpatterns = [
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
