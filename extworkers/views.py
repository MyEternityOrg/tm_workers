import uuid
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from extworkers.forms import CreateRecordForm
from extworkers.models import Enterprises, ExtWorkerRecord
from tm_workers.mixin import BaseClassContextMixin


class PersonRecordModify(UpdateView, BaseClassContextMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/person_edit.html'
    success_url = reverse_lazy('fill_data_shop')
    fields = ['person_name', 'f_time', 't_time']
    # form_class = UpdateRecordForm
    title = 'Редактировать запись'

    def get_form(self, form_class=None):
        form = super(PersonRecordModify, self).get_form()
        form.fields['person_name'].widget.attrs.update(
            {'class': 'special', 'required': True, 'placeholder': "Введите ФИО сотрудника"})
        form.fields['f_time'].widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
        form.fields['t_time'].widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
        return form

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordModify, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        obj = ExtWorkerRecord.objects.filter(dts=datetime.now()).get(guid=self.kwargs.get('pk'))
        obj.person_name = request.POST['person_name']
        obj.f_time = request.POST['f_time']
        obj.t_time = request.POST['t_time']
        obj.save()
        return redirect(reverse_lazy('fill_data_shop', args=(self.kwargs.get('dv'),)))

    # def get_form(self, form_class=None):
    #     form = super(PersonRecordModify, self).get_form()
    #     return form

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form(request.POST)
    #     # post = request.POST.copy()
    #     # post['guid'] = ExtWorkerRecord.objects.get(guid=self.kwargs.get('pk'))
    #     # post['enterprise'] = Enterprises.objects.get(guid=self.kwargs.get('dv'))
    #     # form = UpdateRecordForm(post)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse_lazy('fill_data_shop', args=(self.kwargs.get('dv'),)))
    #     else:
    #         return HttpResponse("Некорректные данные формы!")


class PersonRecordAdd(CreateView, BaseClassContextMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/person_add.html'
    success_url = reverse_lazy('fill_data_shop')
    form_class = CreateRecordForm
    title = 'Добавить сотрудника'

    def get_form(self, form_class=None):
        form = super(PersonRecordAdd, self).get_form()
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
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(enterprise=self.kwargs.get('pk')).filter(dts=datetime.strftime(datetime.now(), '%Y-%m-%d'))

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ShopRecord, self).get_context_data(**kwargs)
        ent = Enterprises.objects.filter(guid=self.kwargs.get('pk')).first()
        context['enterprise'] = ent
        context['dts'] = datetime.strftime(datetime.now(), '%Y-%m-%d')
        context['title'] = ent.name
        return context


class ShopList(ListView):
    model = Enterprises
    template_name = 'extworkers/list_shop.html'
    fields = ['enterprise_code', 'name']
    success_url = reverse_lazy('extworkers/list_shop.html')
    paginate_by = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.get_list_shops()

    def get_context_data(self, **kwargs):
        context = super(ShopList, self).get_context_data(**kwargs)
        context['title'] = 'Список подразделений'
        return context
