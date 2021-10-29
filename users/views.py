from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tm_workers.mixin import BaseClassContextMixin
from users.forms import UserLoginForm
from users.models import ProfileUser


class UserLogout(LogoutView, BaseClassContextMixin):
    model = User
    template_name = '/'


class UserLogin(LoginView, BaseClassContextMixin):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'

    def get(self, request, *args, **kwargs):
        response = super(UserLogin, self).get(request, *args, **kwargs)
        profile = ProfileUser.get_profile_by_user_ip(request.META['REMOTE_ADDR'])
        print(profile)
        if profile:
            user = User.objects.get(pk=profile.user_id)
            login(request, user)
            if user:
                if user.is_active:
                    if user.is_staff:
                        return redirect('tm_workers:fill_data')
                    else:
                        return redirect(reverse_lazy('tm_workers:fill_data_shop', args=(profile.ent_guid,)))
                else:
                    return redirect('users:user_login')
        return response

    def post(self, request, *args, **kwargs):
        auth = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not auth:
            return redirect('users:user_login')
        login(request, auth)
        if auth.is_active:
            if auth.is_staff:
                return redirect('tm_workers:fill_data')
            else:
                profile = ProfileUser.get_profile_by_user_id(auth.id)
                return redirect(reverse_lazy('tm_workers:fill_data_shop', args=(profile.ent_guid,)))
        else:
            return redirect('users:user_login')
