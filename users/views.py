from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from tm_workers.mixin import BaseClassContextMixin
from users.forms import UserLoginForm
from users.models import ProfileUser, Enterprises


class UserLogout(LogoutView, BaseClassContextMixin):
    model = User
    template_name = 'users/logout.html'
    success_url = reverse_lazy('users:login')


class UserMain(ListView, BaseClassContextMixin):
    model = User
    template_name = 'users/index.html'
    title = "Табелирование внешних контрагентов"

    def get_context_data(self, object_list=None, **kwargs):
        context = super(UserMain, self).get_context_data(**kwargs)
        context['dts'] = datetime.strftime(datetime.now(), '%Y-%m-%d')
        try:
            profile = ProfileUser.get_profile_by_user_id(self.request.user.id)
            enterprise = Enterprises.objects.get(guid=profile.ent_guid)
            if enterprise is not None:
                context['enterprise'] = enterprise
        except:
            context['profile_error'] = 'Ошибка сопосталвения подразделения с активным профилем. Проверьте настройки!'
        finally:
            return context


class UserLogin(LoginView, BaseClassContextMixin):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'

    def get(self, request, *args, **kwargs):
        response = super(UserLogin, self).get(request, *args, **kwargs)
        profile = ProfileUser.get_profile_by_user_ip(request.META['REMOTE_ADDR'])
        if profile:
            user = User.objects.get(pk=profile.user_id)
            login(request, user)
            if user:
                if user.is_active:
                    return redirect('users:index')
                    # if user.is_staff:
                    #     return redirect('extworkers:fill_data')
                    # else:
                    #     return redirect(reverse_lazy('extworkers:fill_data_shop', args=(
                    #         profile.ent_guid, datetime.strftime(datetime.now(), '%Y-%m-%d'),)))
                else:
                    return redirect('users:user_login')
        return response

    def post(self, request, *args, **kwargs):
        auth = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not auth:
            return redirect('users:login')
        login(request, auth)
        if auth.is_active:
            return redirect('users:index')
            # if auth.is_staff:
            #     return redirect('extworkers:fill_data')
            # else:
            #     profile = ProfileUser.get_profile_by_user_id(auth.id)
            #     return redirect(reverse_lazy('extworkers:fill_data_shop',
            #                                  args=(profile.ent_guid, datetime.strftime(datetime.now(), '%Y-%m-%d'),)))
        else:
            return redirect('users:login')
