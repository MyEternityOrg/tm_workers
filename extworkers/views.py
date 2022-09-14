import uuid
from datetime import datetime, timedelta, date

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from extworkers.forms import CreateRecordForm
from extworkers.models import Enterprises, ExtWorkerRecord, ExtWorkerRecordHistory
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin


class PersonRecordDelete(DeleteView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    title = 'ПРР: Удалить запись'
    success_url = reverse_lazy('extworkers:shopdata')
    template_name = 'extworkers/extworkers_shop_person_edit.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordDelete, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        context['enterprise'] = Enterprises.objects.get(guid=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        obj = ExtWorkerRecord.objects.get(guid=self.kwargs.get('pk'))
        obj.delete()
        return redirect(reverse_lazy('extworkers:shopdata', args=(self.kwargs.get('dv'), self.kwargs.get('dts'))))


class PersonRecordModify(UpdateView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/extworkers_shop_person_edit.html'
    success_url = reverse_lazy('extworkers:shopdata')
    fields = ['person_name', 'f_time', 't_time', 'p_city', 'p_birthday']
    title = 'ПРР: Редактировать запись'

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
        context['enterprise'] = Enterprises.objects.get(guid=context['extworkerrecord'].enterprise_id)
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
        obj.author = request.user.username
        # obj.author = request.POST[]
        obj.save()
        return redirect(reverse_lazy('extworkers:shopdata', args=(self.kwargs.get('dv'), self.kwargs.get('dts'))))


class PersonRecordAdd(CreateView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/extworkers_shop_person_add.html'
    success_url = reverse_lazy('extworkers:shopdata')
    form_class = CreateRecordForm
    title = 'ПРР: Добавить сотрудника'

    def get_form(self, form_class=None):
        form = super(PersonRecordAdd, self).get_form()
        form.fields['p_birthday'].widget.attrs.update({'data-format': 'yyyy-MM-dd', 'readonly': True, 'required': True})
        return form

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PersonRecordAdd, self).get_context_data(**kwargs)
        context['dts'] = self.kwargs.get('dts')
        context['enterprise'] = Enterprises.objects.get(guid=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['guid'] = uuid.uuid4()
        post['dts'] = datetime.strptime(self.kwargs.get('dts'), '%Y-%m-%d').date()
        post['enterprise'] = Enterprises.objects.get(guid=self.kwargs.get('pk'))
        post['author'] = request.user.username
        form = CreateRecordForm(post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные сохранены!')
            return redirect(
                reverse_lazy('extworkers:shopdata', args=(self.kwargs.get('pk'), self.kwargs.get('dts'))))
        else:
            messages.warning(request, 'Ошибка данных!')
            return HttpResponse("Некорректные данные формы!")


class ShopRecord(ListView, BaseClassContextMixin, UserLoginCheckMixin):
    model = ExtWorkerRecord
    template_name = 'extworkers/extworkers_shop_info.html'
    success_url = reverse_lazy('extworkers:shopdata')
    paginate_by = 10

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
        context['dts_arr'] = dts_arr
        context['title'] = "ПРР: " + ent.name
        if date.today() != datetime.strptime(context['dts'], '%Y-%m-%d').date():
            context['ro'] = True
        else:
            context['ro'] = False
        if self.request.user.is_staff:
            context['history_data'] = ExtWorkerRecordHistory.objects.filter(
                enterprise_guid=ent.guid,
                dts=self.kwargs.get('dts')
            ).order_by('data_guid', '-change_time')
        return context


class ShopList(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = Enterprises
    template_name = 'extworkers/extworkers_shop_list.html'
    fields = ['enterprise_code', 'name']
    success_url = reverse_lazy('extworkers:shoplist')
    paginate_by = 15
    title = 'ПРР: Список подразделений'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        nn = self.request.GET.get('id')
        if nn is not None:
            return self.model.get_list_shops().filter(name__contains=nn)
        else:
            return self.model.get_list_shops()

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ShopList, self).get_context_data(**kwargs)
        context['dts'] = datetime.strftime(datetime.now(), '%Y-%m-%d')
        return context
