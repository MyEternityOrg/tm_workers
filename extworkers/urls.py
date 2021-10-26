from django.urls import path

from .views import ShopList, ShopRecord, PersonRecordAdd, PersonRecordModify, PersonRecordDelete

urlpatterns = [
    path('', ShopList.as_view(), name='fill_data'),
    path('<pk>/', ShopRecord.as_view(), name='fill_data_shop'),
    path('<pk>/add/', PersonRecordAdd.as_view(), name='person_add'),
    path('<dv>/edit/<pk>', PersonRecordModify.as_view(), name='person_edit'),
    path('<dv>/delete/<pk>', PersonRecordDelete.as_view(), name='person_delete')
]
