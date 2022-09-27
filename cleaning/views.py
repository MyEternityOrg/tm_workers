import uuid
import calendar
from datetime import datetime, timedelta, date

from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from cleaning.models import CleaningPlan, CleaningFact
from outsourcing.models import Enterprises
from cleaning.forms import CreateCleaningForm
from cleaning.filters import CleaningFilter


TYPE_ClEANING = '6B28C419-5F57-463D-B364-21C43CB104AA'


class CleaningList(ListView, BaseClassContextMixin, UserLoginCheckMixin):
    model = CleaningPlan
    template_name = 'cleaning/cleaning_list.html'
    context_object_name = 'cleaning_plan'
    paginate_by = 31


    def __init__(self, **kwargs):
        super(CleaningList, self).__init__(**kwargs)
        self.filter_set = None


    def get_queryset(self):
        qs = self.model.objects.all()
        self.filter_set = CleaningFilter(self.request.GET, queryset=qs)

        return self.filter_set.qs.order_by('dts')


    def get_context_data(self, object_list=None, **kwargs):

        init_fact = CleaningFact.objects.all()
        q_f = self.filter_set.data
        dts =q_f.get('dts')
        if dts:
            f_year = int(dts[:4])
            f_month = int(dts[5:7])
            today = date.today()
            if today.month == f_month and today.year == f_year:
                end_day = today.day
            else:
                interval_month = calendar.monthrange(f_year, f_month)
                end_day = interval_month[1]

            init_fact = init_fact.filter(dts__gte=date(f_year, f_month, 1),
                                 dts__lte=date(f_year, f_month, end_day))

        ent = q_f.get('enterprise')
        if ent:
            init_fact = init_fact.filter(enterprise=ent)

        context = super(CleaningList, self).get_context_data(**kwargs)
        context['title'] = "Клининг"

        # init_fact = CleaningFact.objects.filter(enterprise=ent, dts__lte=today, dts__gte=begin_dts)
        init = list(map(lambda i: {'guid': i.guid, 'dts': i.dts, 'enterprise': i.enterprise,
                                   'contractor': i.contractor, 'sheduler': i.sheduler,
                                   'plan_hours': i.plan_hours}, context['cleaning_plan']))

        for i in init:
            list_fact = list(filter(lambda x: x.dts == i['dts']
                                               and x.enterprise == i['enterprise'], init_fact))
            i['hours_f'] = list_fact[0].fact_hours if list_fact else 0

        context['init'] = init
        context['filter'] = self.filter_set

        return context



class CleaningEditCreate(CreateView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = CleaningFact
    template_name = 'cleaning/cleaning_add.html'
    form_class = CreateCleaningForm


    def get_context_data(self, **kwargs):
        context = super(CleaningEditCreate, self).get_context_data(**kwargs)

        obj = CleaningPlan.objects.get(guid=self.request.GET.get('guid'))
        obj_f = CleaningFact.objects.filter(enterprise=obj.enterprise, dts=obj.dts)
        context['obj'] = obj
        context['fact_hours'] = obj_f.last().fact_hours if obj_f else 0

        return context

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()

        obj = CleaningPlan.objects.get(guid=post['obj_guid'])

        post['dts'] = obj.dts
        post['enterprise'] = obj.enterprise

        form = CreateCleaningForm(post)
        if form.is_valid():
            obj = CleaningFact.objects.filter(enterprise=obj.enterprise, dts=obj.dts)
            if obj:
                for i in obj:
                    i.delete()

            form.save()
        return redirect('cleaning:cleaninglist')

