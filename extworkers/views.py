import uuid
from datetime import datetime, timedelta

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from extworkers.forms import CreateRecordForm
from extworkers.models import Enterprises, ExtWorkerRecord
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin

CONST_MAX_TIME = 12


class PersonRecordDelete(DeleteView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    title = 'Удалить запись'
    success_url = reverse_lazy('tm_workers:fill_data_shop')
    template_name = 'extworkers/person_edit.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordDelete, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        context['max_hour'] = CONST_MAX_TIME
        context['staff'] = self.request.user.is_staff
        return context

    def post(self, request, *args, **kwargs):
        obj = ExtWorkerRecord.objects.filter(dts=self.kwargs.get('dts')).get(guid=self.kwargs.get('pk'))
        obj.delete()
        return redirect(reverse_lazy('tm_workers:fill_data_shop', args=(self.kwargs.get('dv'), self.kwargs.get('dts'))))


class PersonRecordModify(UpdateView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/person_edit.html'
    success_url = reverse_lazy('tm_workers:fill_data_shop')
    fields = ['person_name', 'f_time', 't_time', 'p_city', 'p_birthday']
    title = 'Редактировать запись'

    def get_form(self, form_class=None):
        form = super(PersonRecordModify, self).get_form()
        form.fields['person_name'].widget.attrs.update(
            {'class': 'special', 'required': True, 'placeholder': "Введите ФИО сотрудника"})
        form.fields['f_time'].widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
        form.fields['t_time'].widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
        form.fields['p_city'].widget.attrs.update(
            {'class': 'special', 'required': True, 'placeholder': "Место рождения сотрудника"})
        form.fields['p_birthday'].widget.attrs.update({'data-format': 'yyyy-MM-dd', 'readonly': True, 'required': True})
        return form

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordModify, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        context['max_hour'] = CONST_MAX_TIME
        context['staff'] = self.request.user.is_staff
        return context

    def post(self, request, *args, **kwargs):
        obj = ExtWorkerRecord.objects.filter(dts=datetime.strptime(self.kwargs.get('dts'), '%Y-%m-%d')).get(
            guid=self.kwargs.get('pk'))
        obj.person_name = request.POST['person_name']
        obj.dts = datetime.strptime(self.kwargs.get('dts'), '%Y-%m-%d').date()
        obj.f_time = request.POST['f_time']
        obj.t_time = request.POST['t_time']
        obj.p_birthday = request.POST['p_birthday']
        obj.p_city = request.POST['p_city']
        obj.save()
        return redirect(reverse_lazy('tm_workers:fill_data_shop', args=(self.kwargs.get('dv'), self.kwargs.get('dts'))))


class PersonRecordAdd(CreateView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/person_add.html'
    success_url = reverse_lazy('tm_workers:fill_data_shop')
    form_class = CreateRecordForm
    title = 'Добавить сотрудника'

    def get_form(self, form_class=None):
        form = super(PersonRecordAdd, self).get_form()
        form.fields['p_birthday'].widget.attrs.update({'data-format': 'yyyy-MM-dd', 'readonly': True, 'required': True})
        return form

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordAdd, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        context['max_hour'] = CONST_MAX_TIME
        context['staff'] = self.request.user.is_staff
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()
        post['dts'] = datetime.strptime(self.kwargs.get('dts'), '%Y-%m-%d').date()
        post['enterprise'] = Enterprises.objects.get(guid=self.kwargs.get('pk'))
        form = CreateRecordForm(post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные сохранены!')
            return redirect(
                reverse_lazy('tm_workers:fill_data_shop', args=(self.kwargs.get('pk'), self.kwargs.get('dts'))))
        else:
            messages.warning(request, 'Ошибка данных!')
            return HttpResponse("Некорректные данные формы!")


class ShopRecord(ListView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/fill_shop.html'
    success_url = reverse_lazy('tm_workers:fill_data')
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(enterprise=self.kwargs.get('pk'), dts=datetime.strptime(self.kwargs.get('dts'), '%Y-%m-%d'))

    def get_context_data(self, object_list=None, **kwargs):
        dts_arr = []
        for i in range(-7, 1):
            dts_arr.append(
                datetime.strftime(datetime.now().date() + timedelta(days=i), '%Y-%m-%d'))

        context = super(ShopRecord, self).get_context_data(**kwargs)
        ent = Enterprises.objects.get(guid=self.kwargs.get('pk'))
        context['enterprise'] = ent
        context['dts'] = self.kwargs.get('dts')
        context['max_hour'] = CONST_MAX_TIME
        context['dts_arr'] = dts_arr
        context['staff'] = self.request.user.is_staff
        context['title'] = ent.name
        return context


class ShopList(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = Enterprises
    template_name = 'extworkers/list_shop.html'
    fields = ['enterprise_code', 'name']
    success_url = reverse_lazy('extworkers/list_shop.html')
    paginate_by = 30
    title = 'Список подразделений'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.get_list_shops()

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ShopList, self).get_context_data(**kwargs)
        context['dts'] = datetime.strftime(datetime.now(), '%Y-%m-%d')
        context['max_hour'] = CONST_MAX_TIME
        context['staff'] = self.request.user.is_staff
        return context
