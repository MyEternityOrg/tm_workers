from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from outsourcing.forms import CreatePriceForm, CreatePlanningRecordForm
from outsourcing.models import *
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from .filters import PlanningStaffFilter, PlanningPricesFilter


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
        super(OutsourcingTimeline, self).__init__(**kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('name')


class OutsourcingTimelineData(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTimelineData
    template_name = 'outsourcing_timeline_data.html'
    success_url = reverse_lazy('outsourcing:outsourcing_timeline')
    title = 'Детали графика'
    paginate_by = 15

    def __init__(self, **kwargs):
        super(OutsourcingTimelineData, self).__init__(**kwargs)

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

    def __init__(self, **kwargs):
        super(OutsourcingPrices, self).__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        arr = self.model.objects.raw(
            "select * from [get_outsourcing_prices_offset] (%s)", [datetime.datetime.today()])
        qr = self.model.objects.filter(guid__in=[x.guid for x in arr])
        self.filter_set = PlanningPricesFilter(self.request.GET, queryset=qr)
        return self.filter_set.qs.order_by('enterprise__name')

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutsourcingPrices, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        context[
            'filtered_path'] = f"?contractor={self.request.GET.get('contractor', '')}&enterprise={self.request.GET.get('enterprise', '')}"
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
    paginate_by = 15

    def __init__(self, **kwargs):
        super(OutSourcingPlanningStaff, **kwargs).__init__(**kwargs)
        self.filter_set = None

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OutSourcingPlanningStaff, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        context[
            'filtered_path'] = f"?contractor={self.request.GET.get('contractor', '')}&enterprise={self.request.GET.get('enterprise', '')}"
        return context

    def get_queryset(self):
        arr = self.model.objects.raw(
            "select guid from [get_outsourcing_pplanning_offset] (%s) order by dts",
            [datetime.datetime.today()])
        qr = self.model.objects.filter(guid__in=[x.guid for x in arr])
        self.filter_set = PlanningStaffFilter(self.request.GET, queryset=qr)
        return self.filter_set.qs.order_by('enterprise__name')


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
