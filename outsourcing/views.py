import uuid
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from tm_workers.mixin import BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from outsourcing.models import *


class OutsourcingIndex(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    #model = OutsourcingTypes
    template_name = 'outsourcing_index.html'
    success_url = reverse_lazy('outsourcing:outsourcing_index')


class OutsourcingTypes(ListView, BaseClassContextMixin, UserLoginCheckMixin, UserIsAdminCheckMixin):
    model = OutsourcingTypes
    template_name = 'outsourcing_types.html'
    success_url = reverse_lazy('outsourcing:outsourcing_index')

