import uuid
import calendar
from datetime import datetime, timedelta, date

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from security.models import SecurityPlan, SecurityFact
from outsourcing.models import Enterprises
from security.forms import SecurityForm
from security.filters import SecurityFilter
from users.models import ProfileUser


class SecurityList(ListView, BaseClassContextMixin, UserLoginCheckMixin):
    model = SecurityPlan
    template_name = 'security/security_list.html'
    context_object_name = 'security_plan'
    paginate_by = 31

    def __init__(self, **kwargs):
        kwargs['fl_security'] = True
        super(SecurityList, self).__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        qs = self.model.objects.all()
        self.filter_set = SecurityFilter(self.request.GET, queryset=qs)

        if not self.request.user.is_staff:
            q_f = self.filter_set.data
            if q_f:
                q_f._mutable = True
            q_f['enterprise'] = ProfileUser.get_profile_by_user_id(self.request.user.id).ent_guid
            if not q_f.get('dts'):
                q_f['dts'] = date.today().strftime('%Y-%m')

        return self.filter_set.qs.order_by('dts')

    def get_context_data(self, object_list=None, **kwargs):
        today = date.today()

        init_fact = SecurityFact.objects.all()
        q_f = self.filter_set.data
        dts = q_f.get('dts')
        if dts:
            f_year = int(dts[:4])
            f_month = int(dts[5:7])

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

        context = super(SecurityList, self).get_context_data(**kwargs)
        context['title'] = "ЧОП"

        init = list(map(lambda i: {'guid': i.guid, 'dts': i.dts, 'enterprise': i.enterprise,
                                   'contractor': i.contractor, 'sheduler': i.sheduler,
                                   'plan_hours': i.plan_hours}, context['security_plan']))

        for i in init:
            list_fact = list(filter(lambda x: x.dts == i['dts']
                                              and x.enterprise == i['enterprise'], init_fact))
            i['hours_f'] = list_fact[0].fact_hours if list_fact else 0

        context['init'] = init
        context['filter'] = self.filter_set
        context['today'] = today

        # Для общего шаблона...
        if not self.request.user.is_staff:
            context['enterprise'] = Enterprises.objects.get(
                guid=ProfileUser.get_profile_by_user_id(self.request.user.id).ent_guid)
            context['dts'] = today

        return context


class SecurityEditCreate(CreateView, BaseClassContextMixin, UserLoginCheckMixin):
    model = SecurityFact
    template_name = 'security/security_add.html'
    form_class = SecurityForm

    def __init__(self, **kwargs):
        kwargs['fl_security'] = True
        super(SecurityEditCreate, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(SecurityEditCreate, self).get_context_data(**kwargs)

        obj = SecurityPlan.objects.get(guid=self.request.GET.get('guid'))
        obj_f = SecurityFact.objects.filter(enterprise=obj.enterprise, dts=obj.dts)
        context['obj'] = obj
        context['fact_hours'] = obj_f.last().fact_hours if obj_f else 0

        return context

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()

        obj = SecurityPlan.objects.get(guid=post['obj_guid'])

        post['dts'] = obj.dts
        post['enterprise'] = obj.enterprise

        form = SecurityForm(post)
        if form.is_valid():
            obj = SecurityFact.objects.filter(enterprise=obj.enterprise, dts=obj.dts)
            if obj:
                for i in obj:
                    i.delete()

            form.save()
        return redirect('security:securitylist')


def save_security(request):
    post = {}
    post['guid'] = uuid.uuid4()

    obj = SecurityPlan.objects.get(guid=request.POST.get('obj_guid'))

    post['dts'] = obj.dts
    post['enterprise'] = obj.enterprise
    post['fact_hours'] = request.POST.get('hours')

    form = SecurityForm(post)
    if form.is_valid():
        obj = SecurityFact.objects.filter(enterprise=obj.enterprise, dts=obj.dts)
        if obj:
            for i in obj:
                i.delete()

        form.save()
        return JsonResponse({'result': 1})
    else:
        return JsonResponse({'result': 0})
