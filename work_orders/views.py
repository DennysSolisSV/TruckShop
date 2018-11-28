from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView, ListView
from django.contrib.auth.models import Group

from timecard.models import TimeDay
from .models import MechachicTimeTask, Task, WorkOrder

from datetime import date
today = date.today()


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

        # getting registers of the tasks. For to the user mechanic
        task_obj = Task.objects.get_by_user(self.request)

        # getting registers for today where the mechanic marked time
        timecard = TimeDay.objects.filter(
            user=self.request.user, time__contains=today).order_by('time')

        # getting lastest register for the mechanic, it can be when he clock in or clock out
        try:
            time = TimeDay.objects.latest('time')
        except TimeDay.DoesNotExist:
            time = None

        try:
            currency = MechachicTimeTask.objects.filter(
                user=self.request.user, time__contains=today).latest('time')
        except MechachicTimeTask.DoesNotExist:
            currency = None

        context = {
            'task': task_obj,
            'timecard': timecard,
            'time': time,
            'currency': currency,
        }
        return context


class WorkOrderView(LoginRequiredMixin, ListView):
    template_name = 'work_orders/index.html'
    queryset = WorkOrder.objects.all()

class WorkOrderdetailView(DetailView):
    queryset = WorkOrder.objects.all()
    template_name =  'work_orders/work_order.html'


def clock_in(request):
    time = TimeDay.objects.create(user=request.user, clock_in=True)
    return redirect('work_orders:index')


def clock_out(request):
    time = TimeDay.objects.create(user=request.user, clock_in=False)
    return redirect('work_orders:index')


def start_or_end_task(request):
    query = request.GET.get('q', None)
    query2 = request.GET.get('type', None)

    if query2 == 'start':
        clockin = True
    else:
        clockin = False

    if query is not None:
        task = Task.objects.get(id=query)
        MechachicTimeTask.objects.create(
            task=task, user=request.user, clock_in=clockin)
    return redirect('work_orders:index')


def check_group(user, name_group):
    if user.groups.filter(name=name_group).exists():
        return True
    else:
        return False
