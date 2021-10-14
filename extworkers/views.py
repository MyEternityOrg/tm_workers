import uuid
from datetime import datetime

from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from extworkers.forms import CreateRecordForm
from extworkers.models import Enterprises, ExtWorkerRecord


class PersonRecordAdd(CreateView):
    model = ExtWorkerRecord
    template_name = 'extworkers/person_add.html'
    success_url = reverse_lazy('fill_data_shop')
    form_class = CreateRecordForm

    # fields = [
    #     'guid',
    #     'enterprise_guid',
    #     'person_name',
    #     'f_time',
    #     't_time',
    #     'duration'
    # ]

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordAdd, self).get_context_data(**kwargs)
        context['title'] = 'Добавить сотрудника'
        return context

    def post(self, request, *args, **kwargs):
        ret_url = reverse_lazy('fill_data_shop', args=(self.kwargs.get('uid'),))
        form = CreateRecordForm(request.POST)
        for f in form.fields:
            print(form.fields[f])
        return redirect(ret_url)


class ShopRecord(ListView):
    model = ExtWorkerRecord
    template_name = 'extworkers/fill_shop.html'
    fields = ['guid',
              'enterprise_guid',
              'dts',
              'person_name',
              'f_time',
              't_time',
              'duration']
    success_url = reverse_lazy('fill_data')

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ShopRecord, self).get_context_data(**kwargs)
        self.pk = self.kwargs.get('pk')
        filtrate_dts = datetime.strftime(datetime.now(), '%Y-%m-%d')
        ent = Enterprises.objects.get(guid=self.pk)
        context['enterprise'] = ent
        context['dts'] = filtrate_dts
        context['object_list'] = self.model.objects.filter(enterprise_guid=self.pk).filter(dts=filtrate_dts)
        context['title'] = ent.name
        return context


class ShopList(ListView):
    model = Enterprises
    template_name = 'extworkers/list_shop.html'
    fields = ['enterprise_code', 'name']
    success_url = reverse_lazy('extworkers/list_shop.html')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.get_list_shops(self.model)

    def get_context_data(self, **kwargs):
        context = super(ShopList, self).get_context_data(**kwargs)
        context['title'] = 'Список подразделений'
        return context
