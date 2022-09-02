"""tm_workers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from outsourcing.views import *


app_name = 'outsourcing'

urlpatterns = [
                path('types/', OutsourcingTypes.as_view(), name='outsourcing_types'),
                path('prices/', OutsourcingPrices.as_view(), name='outsourcing_prices'),
                path('prices/add', OutSourcingPricesAdd.as_view(), name='outsourcing_prices_add'),
                path('contractors/', OutsourcingContractors.as_view(), name='outsourcing_contractors'),
                path('timeline/', OutsourcingTimeline.as_view(), name='outsourcing_timeline'),
                path('planning/', OutsourcingDataP.as_view(), name='outsourcing_datap'),
                path('planning_staff/', OutSourcingPlanningStaff.as_view(), name='outsourcing_planning_staff'),
                path('planning_staff/add', OutSourcingPlanningStaffAdd.as_view(), name='outsourcing_planning_staff_add'),
                path('timeline_data/<pk>', OutsourcingTimelineData.as_view(), name='outsourcing_timeline_data'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)