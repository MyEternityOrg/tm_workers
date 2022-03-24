from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import ShopList, ShopRecord, PersonRecordAdd, PersonRecordModify, PersonRecordDelete

app_name = 'tm_workers'

urlpatterns = [
                  path('', ShopList.as_view(), name='fill_data'),
                  path('<pk>/<dts>/', ShopRecord.as_view(), name='fill_data_shop'),
                  path('<pk>/<dts>/add/', PersonRecordAdd.as_view(), name='person_add'),
                  path('<dv>/<dts>/edit/<pk>', PersonRecordModify.as_view(), name='person_edit'),
                  path('<dv>/<dts>/delete/<pk>', PersonRecordDelete.as_view(), name='person_delete')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
