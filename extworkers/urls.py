from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from .views import ShopList, ShopRecord

urlpatterns = [
    path('', ShopList.as_view(), name='fill_data'),
    path('<pk>/', ShopRecord.as_view(), name='fill_data_shop'),
]