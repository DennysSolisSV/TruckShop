from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.models import Group

from .models import Task


class MainView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = request.user
        # verify that the user is mechanic
        if check_group(user, 'Mechanics'):
            return redirect('work_orders:time_card')
        else:
            return redirect('work_orders:order')


class TimeCardView(LoginRequiredMixin, TemplateView):
    template_name = 'work_orders/index2.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TimeCardView, self).get_context_data(
            *args, **kwargs)
        task_obj = Task.objects.get_by_user(self.request)
        context['tasks'] = task_obj
        print(context['tasks'])  # '
        return context


class WorkOrderView(LoginRequiredMixin, View):
    pass


def clock_in(request):
    return redirect('work_orders:index')


def clock_out(request):
    return redirect('work_orders:index')


def check_group(user, name_group):
    if user.groups.filter(name=name_group).exists():
        return True
    else:
        return False
