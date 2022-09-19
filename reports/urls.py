from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from reports.views import *


app_name = 'reports'

urlpatterns = [
                path('actservices/', report_act_service, name='report_act_service'),
                path('select_contractor/', select_contractor, name='select_contractor'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)