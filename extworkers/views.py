import uuid
from datetime import datetime, timedelta

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from extworkers.forms import CreateRecordForm
from extworkers.models import Enterprises, ExtWorkerRecord
from tm_workers.mixin import BaseClassContextMixin


class PersonRecordAdd(CreateView, BaseClassContextMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/person_add.html'
    success_url = reverse_lazy('fill_data_shop')
    form_class = CreateRecordForm
    title = 'Добавить сотрудника'

    def get_form(self, form_class=None):
        form = super(PersonRecordAdd, self).get_form()
        form.person_name = 'Иванов Иван Иванович'
        return form

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()
        post['enterprise'] = Enterprises.objects.get(guid=self.kwargs.get('pk'))
        form = CreateRecordForm(post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные сохранены!')
            return redirect(reverse_lazy('fill_data_shop', args=(self.kwargs.get('pk'),)))
        else:
            messages.warning(request, 'Ошибка данных!')
            return HttpResponse("Некорректные данные формы!")


class ShopRecord(ListView):
    model = ExtWorkerRecord
    template_name = 'extworkers/fill_shop.html'
    success_url = reverse_lazy('fill_data')

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ShopRecord, self).get_context_data(**kwargs)
        filtrate_dts = datetime.strftime(datetime.now(), '%Y-%m-%d')

        g = uuid.UUID(self.kwargs.get("pk"))
        print(g)

        ent = Enterprises.objects.filter(guid=self.kwargs.get('pk')).first()
        context['enterprise'] = ent
        context['dts'] = filtrate_dts
        context['object_list'] = self.model.objects.filter(enterprise=self.kwargs.get('pk')).filter(dts=filtrate_dts)
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
        return self.model.get_list_shops()

    def get_context_data(self, **kwargs):
        context = super(ShopList, self).get_context_data(**kwargs)
        context['title'] = 'Список подразделений'
        return context
