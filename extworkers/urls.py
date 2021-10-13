from django.urls import path

from .views import ShopList, ShopRecord, PersonRecordAdd

urlpatterns = [
    path('', ShopList.as_view(), name='fill_data'),
    path('<pk>/', ShopRecord.as_view(), name='fill_data_shop'),
    path('<uid>/add/', PersonRecordAdd.as_view(), name='person_add'),
]
