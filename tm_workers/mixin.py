from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin

from users.models import ProfileUser

CONST_MAX_TIME = 12
CONST_MAX_HOURS = 10

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
        try:
            fl_cleaning = self.fl_cleaning
        except:
            fl_cleaning = False
        try:
            fl_security = self.fl_security
        except:
            fl_security = False



        if request.user.is_active:
            if request.user.is_staff and dts <= datetime.now().date():
                return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
            elif fl_cleaning or fl_security:
                return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
            else:
                if (profile.ent_guid == kwargs.get('dv') or profile.ent_guid == kwargs.get(
                        # 'pk')) and dts == datetime.now().date():
                        'pk')):
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
        context['max_hour'] = CONST_MAX_TIME
        context['max_hours'] = CONST_MAX_HOURS
        return context
