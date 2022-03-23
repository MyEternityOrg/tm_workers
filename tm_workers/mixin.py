from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin

from users.models import ProfileUser


class UserIsAdminCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsAdminCheckMixin, self).dispatch(request, *args, **kwargs)


class UserLoginCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        dts = datetime.now().date()
        dts_str = self.kwargs.get('dts')
        if dts_str is not None:
            dts = datetime.strptime(dts_str, '%Y-%m-%d').date()
        profile = ProfileUser.get_profile_by_user_id(request.user.id)

        if request.user.is_active:
            if request.user.is_staff and dts <= datetime.now().date():
                return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
            else:
                if (profile.ent_guid == kwargs.get('dv') or profile.ent_guid == kwargs.get(
                        'pk')) and dts == datetime.now().date():
                    return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
                else:
                    return HttpResponseNotAllowed(request.method)
        else:
            return HttpResponseNotAllowed(request.method)


class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
