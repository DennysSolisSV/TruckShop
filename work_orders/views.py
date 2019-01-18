from datetime import date
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView

from .forms import WorkOrderForm, TaskForm, PartsByTaskForm
from .models import MechachicTimeTask, Task, WorkOrder, PartsByTask
from timecard.models import TimeDay
from truckshop.utils import unique_work_order_number_generator


today = date.today()

# Redirect depend of the group for the user


class MainView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = request.user
        # verify that the user is mechanic
        if check_group(user, 'Mechanics'):
            return redirect('work_orders:time_card')
        else:
            return redirect('search:query')


class TimeCardView(LoginRequiredMixin, TemplateView):
    template_name = 'work_orders/index2.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TimeCardView, self).get_context_data(
            *args, **kwargs)

        # Getting registers of the tasks. For to the user mechanic
        task_obj = Task.objects.get_by_user(self.request)

        # Getting registers for today where the mechanic marked time
        timecard = TimeDay.objects.filter(
            user=self.request.user, time__contains=today).order_by('time')

        # Getting lastest register for the mechanic,
        # it can be when he clock in or clock out
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

# Creating a work order


class WorkOrderCreateView(TemplateView):
    template_name = 'work_orders/work_order_form.html'

    def get(self, request, *args, **kwargs):
        # creating a instance to pass it to the function
        work_order = WorkOrder.objects.first()
        new_work_order = unique_work_order_number_generator(work_order)
        data = {"number_order": new_work_order}
        work_form = WorkOrderForm(initial=data)
        context = {
            "work_form": work_form,
        }
        return render(request, self.template_name, context)


class WorkOrderdetailView(DetailView):
    template_name = 'work_orders/work_order_form.html'

    def get(self, request, slug, *args, **kwargs):
        work_order = WorkOrder.objects.get(slug=slug)
        tasks = Task.objects.filter(work_order=work_order)
        data = {
            "number_order": work_order.number_order,
            "client": work_order.client,
            "truck": work_order.truck,
        }

        work_form = WorkOrderForm(initial=data)
        context = {
            "work_form": work_form,
            "tasks": tasks,
        }
        return render(request, self.template_name, context)


class TaskDetailView(DetailView):
    template_name = 'work_orders/task_detail.html'

    def get(self, request, pk, *args, **kwargs):
        task = Task.objects.get(pk=pk)
        parts = PartsByTask.objects.filter(task=task)
        data = {
            "work_order": task.work_order.number_order,
            "title": task.title,
            "description": task.description,
            "time_labor": task.time_labor,
            "mechanic": task.mechanic,
        }

        task_form = TaskForm(initial=data)
        context = {
            "task_form": task_form,
            "parts": parts,
            "task_pk": pk,
        }
        return render(request, self.template_name, context)


class AddPartsCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'work_orders/parts_form.html'
    form_class = PartsByTaskForm
    success_message = 'Success: Part was added.'
    success_url = reverse_lazy('work_orders:task_detail')

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        obj = form.save(commit=False)
        obj.task = task
        return super(AddPartsCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        url = reverse("work_orders:task_detail", kwargs={"pk": pk})
        return url


def clock_in(request):
    time = TimeDay.objects.create(
        user=request.user, clock_in=True)
    return redirect('work_orders:index')


def clock_out(request):
    time = TimeDay.objects.create(
        user=request.user, clock_in=False)
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
