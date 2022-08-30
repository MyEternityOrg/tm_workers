import uuid
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

import extworkers.models
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from outsourcing.models import *


class OutsourcingTypes(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTypes
    template_name = 'outsourcing_types.html'
    success_url = reverse_lazy('outsourcing:outsourcing_types')
    title = 'Виды контрагентов'
    paginate_by = 30


class OutsourcingContractors(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingContractors
    template_name = 'outsourcing_contractors.html'
    success_url = reverse_lazy('outsourcing:outsourcing_contractors')
    title = 'Соответствие контрагентов'
    paginate_by = 30


class OutsourcingTimeline(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTimeline
    template_name = 'outsourcing_timeline.html'
    success_url = reverse_lazy('outsourcing:outsourcing_timeline')
    title = 'Графики контрагентов'
    paginate_by = 30


class OutsourcingTimelineData(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTimelineData
    template_name = 'outsourcing_timeline_data.html'
    success_url = reverse_lazy('outsourcing:outsourcing_timeline')
    title = 'Детали графика'
    paginate_by = 30


class OutsourcingDataP(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingDataP
    template_name = 'outsourcing_datap.html'
    success_url = reverse_lazy('outsourcing:outsourcing_datap')
    title = 'Распределение контрагентов'
    paginate_by = 30


class OutsourcingPrices(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingPrices
    template_name = 'outsourcing_prices.html'
    success_url = reverse_lazy('outsourcing:outsourcing_prices')
    title = 'Цены контрагентов'
    paginate_by = 30

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutsourcingPrices, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        return context
