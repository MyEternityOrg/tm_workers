from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from outsourcing.views import *
from outsourcing.filters import PlanningStaffFilter
from django_filters.views import FilterView

app_name = 'outsourcing'

urlpatterns = [
                  path('types/', OutsourcingTypes.as_view(), name='outsourcing_types'),
                  path('prices/', OutsourcingPrices.as_view(), name='outsourcing_prices'),
                  path('prices/add', OutSourcingPricesAdd.as_view(), name='outsourcing_prices_add'),
                  path('contractors/', OutsourcingContractors.as_view(), name='outsourcing_contractors'),
                  path('timeline/', OutsourcingTimeline.as_view(), name='outsourcing_timeline'),
                  path('planning/', OutsourcingDataP.as_view(), name='outsourcing_datap'),
                  path('planning_staff/search/', OutSourcingPlanningStaff.as_view(), name='outsourcing_planning_staff'),
                  # path('planning_staff/search/', FilterView.as_view(filterset_class=PlanningStaffFilter, template_name='outsourcing_planning.html'),
                  #      name='outsourcing_planning_staff'),
                  path('planning_staff/add', OutSourcingPlanningStaffAdd.as_view(),
                       name='outsourcing_planning_staff_add'),
                  path('timeline_data/<pk>', OutsourcingTimelineData.as_view(), name='outsourcing_timeline_data'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
