import uuid
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

import extworkers.models
from outsourcing.forms import CreatePriceForm
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from outsourcing.models import *


class OutsourcingTypes(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTypes
    template_name = 'outsourcing_types.html'
    success_url = reverse_lazy('outsourcing:outsourcing_types')
    title = 'Виды контрагентов'
    paginate_by = 15

    def get_queryset(self):
        return self.model.objects.all().order_by('name')


class OutsourcingContractors(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingContractors
    template_name = 'outsourcing_contractors.html'
    success_url = reverse_lazy('outsourcing:outsourcing_contractors')
    title = 'Соответствие контрагентов'
    paginate_by = 15

    def get_queryset(self):
        return self.model.objects.all().order_by('name')


class OutsourcingTimeline(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTimeline
    template_name = 'outsourcing_timeline.html'
    success_url = reverse_lazy('outsourcing:outsourcing_timeline')
    title = 'Графики контрагентов'
    paginate_by = 15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('name')

class OutsourcingTimelineData(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTimelineData
    template_name = 'outsourcing_timeline_data.html'
    success_url = reverse_lazy('outsourcing:outsourcing_timeline')
    title = 'Детали графика'
    paginate_by = 15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(outsourcing_timeline=self.kwargs.get('pk')).order_by('dts')


class OutsourcingDataP(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingDataP
    template_name = 'outsourcing_datap.html'
    success_url = reverse_lazy('outsourcing:outsourcing_datap')
    title = 'Распределение контрагентов'
    paginate_by = 15

    def get_queryset(self):
        return self.model.objects.all().order_by('outsourcing_contractor', 'dts', 'enterprise')


class OutsourcingPrices(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingPrices
    template_name = 'outsourcing_prices.html'
    success_url = reverse_lazy('outsourcing:outsourcing_prices')
    title = 'Цены контрагентов'
    paginate_by = 15

    def get_queryset(self):
        return self.model.objects.all().order_by('contractor')

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutsourcingPrices, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        return context


class OutSourcingPricesAdd(CreateView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingPrices
    template_name = 'outsourcing_prices_add.html'
    title = 'Добавить запись'
    success_url = reverse_lazy('outsourcing:outsourcing_prices')
    form_class = CreatePriceForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutSourcingPricesAdd, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class=None):
        form = super(OutSourcingPricesAdd, self).get_form()
        return form

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        form = CreatePriceForm(post)
        if form.is_valid():
            form.save()
        return redirect('outsourcing:outsourcing_prices')