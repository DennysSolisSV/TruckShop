from datetime import date
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView, TemplateView,
)


from .forms import WorkOrderForm

from .models import MechachicTimeTask, Task, WorkOrder
from timecard.models import TimeDay
from truckshop.utils import unique_work_order_number_generator
from truck.models import Truck


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


class WorkOrderCreateView(CreateView):
    template_name = 'work_orders/work_order_form.html'
    model = WorkOrder
    form_class = WorkOrderForm

    def get_context_data(self, **kwargs):

        context = {
            "work_order_pk": 0,
        }

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url(self, **kwargs):
        urls = reverse("work_orders:detail", kwargs={
            "slug": self.object.slug})
        return urls


class WorkOrderUpdateView(UpdateView):
    template_name = 'work_orders/work_order_form.html'
    model = WorkOrder
    form_class = WorkOrderForm

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        work_order = WorkOrder.objects.get(slug=slug)
        tasks = Task.objects.filter(work_order=work_order).order_by("id")

        context = {
            "tasks": tasks,
        }
        self.request.session['work_order_id'] = work_order.id
        self.request.session['work_order_slug'] = work_order.slug

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url(self, **kwargs):
        url = reverse("work_orders:index")
        return url


# class WorkOrderdetailView(DetailView):
#     template_name = 'work_orders/work_order_form.html'

#     def get(self, request, slug, *args, **kwargs):
#         work_order = WorkOrder.objects.get(slug=slug)
#         tasks = Task.objects.filter(work_order=work_order).order_by("id")
#         data = {
#             "number_order": work_order.number_order,
#             "client": work_order.client,
#             "truck": work_order.truck,
#         }

#         request.session['work_order_id'] = work_order.id
#         request.session['work_order_slug'] = work_order.slug

#         work_form = WorkOrderForm(initial=data)
#         context = {
#             "work_form": work_form,
#             "tasks": tasks,
#         }
#         return render(request, self.template_name, context)


def clock_in(request):
    TimeDay.objects.create(user=request.user, clock_in=True)
    return redirect('work_orders:index')


def clock_out(request):
    TimeDay.objects.create(user=request.user, clock_in=False)
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


def task_time_labor_update_api(request):
    time_labor = request.POST.get("time_labor")
    task_pk = request.POST.get("task_pk")
    print(task_pk)
    if not time_labor.isalpha():
        if task_pk != '0':
            qs = Task.objects.get(pk=task_pk)
            qs.time_labor = time_labor
            qs.save()

            task_data = {
                "total_parts": qs.total_parts,
                "total_labor": qs.total_labor,
                "total_task": qs.total_task
            }
        else:
            total_labor = Decimal(time_labor) * 125
            task_data = {
                "total_parts": '0',
                "total_labor": total_labor,
                "total_task": total_labor
            }

    return JsonResponse(task_data)


def load_trucks(request):
    client_id = request.GET.get('client')
    trucks = Truck.objects.filter(
        client_id=client_id).order_by('fleet')
    print(trucks)
    return render(request, 'snippets/truck_dropdown_list_options.html', {
        'trucks': trucks
    })
