from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import CleaningList, CleaningEditCreate, save_cleaning

app_name = 'cleaning'

urlpatterns = [
                  path('', CleaningList.as_view(), name='cleaninglist'),
                  path('edit', CleaningEditCreate.as_view(), name='cleaning_edit_create'),
                  path('ajax_save_cleaning', save_cleaning, name='ajax_save_cleaning'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
