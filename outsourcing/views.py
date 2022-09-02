import uuid
from django.db.models import Max
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

import extworkers.models
from outsourcing.forms import CreatePriceForm, CreatePlanningRecordForm
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
        return self.model.objects.raw("select * from [get_outsourcing_prices_offset] (%s)", [datetime.datetime.today()])

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

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()
        dts = datetime.datetime.strptime(str(post['dts']), '%Y-%m-%dT%H:%M')
        post['dts'] = dts
        form = CreatePriceForm(post)
        if form.is_valid():
            form.save()
        return redirect('outsourcing:outsourcing_prices')


class OutSourcingPlanningStaff(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingPPlanning
    template_name = 'outsourcing_planning.html'
    title = 'Плановая явка контрагентов'
    success_url = reverse_lazy('outsourcing:outsourcing_planning_staff')

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutSourcingPlanningStaff, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.model.objects.raw("select * from [get_outsourcing_pplanning_offset] (%s)",
                                      [datetime.datetime.today()])


class OutSourcingPlanningStaffAdd(CreateView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutSourcingPlanningStaff
    template_name = 'outsourcing_planning_add.html'
    title = 'Добавить запись'
    success_url = reverse_lazy('outsourcing:outsourcing_planning_staff')
    form_class = CreatePlanningRecordForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutSourcingPlanningStaffAdd, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()
        dts = datetime.datetime.strptime(str(post['dts']), '%Y-%m-%dT%H:%M')
        post['dts'] = dts
        form = CreatePlanningRecordForm(post)
        if form.is_valid():
            form.save()
        return redirect('outsourcing:outsourcing_planning_staff')
