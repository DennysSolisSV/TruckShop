from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView,
    DeleteView
)

from bootstrap_modal_forms.generic import (
  BSModalCreateView,
  BSModalUpdateView,
  BSModalReadView,
  BSModalDeleteView
)

from django.contrib import messages

from work_orders.forms import TaskForm, PartsByTaskForm
from inventory.models import Part
from work_orders.models import Task, PartsByTask, WorkOrder


class TaskCreateView(CreateView):
    template_name = 'task_orders/task_detail.html'
    queryset = Task.objects.all()
    form_class = TaskForm

    def get_initial(self):
        initial_data = super(TaskCreateView, self).get_initial()
        work_order = WorkOrder.objects.get(
            id=self.request.session.get("work_order_id", None))
        initial_data['work_order'] = work_order
        return initial_data

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        task = self.kwargs.get('pk')
        parts = PartsByTask.objects.filter(task=task)

        context = {
            "parts": parts,
            "task_pk": 0,
        }

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url(self, **kwargs):
        urls = reverse("work_orders:update_task", kwargs={
            "pk": self.object.id})
        return urls


class TaskUpdateView(UpdateView):
    template_name = 'task_orders/task_detail.html'
    queryset = Task.objects.all()
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        task = self.kwargs.get('pk')
        parts = PartsByTask.objects.filter(task=task)

        context = {
            "parts": parts,
            "task_pk": self.kwargs.get('pk'),
        }

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url(self, **kwargs):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        url = reverse("work_orders:detail", kwargs={
                      "slug": task.work_order.slug})
        return url


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete_form.html'
    success_message = 'Success: Task was deleted.'

    def get_success_url(self, **kwargs):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        url = reverse("work_orders:detail", kwargs={
                      "slug": task.work_order.slug})
        return url

    def get_context_data(self, **kwargs):
        # Modal title
        context = {
            "message": "Are you sure you want to delete this task",
            "title": "Delete task"
        }
        context.update(kwargs)
        return super(TaskDeleteView, self).get_context_data(**context)


class AddPartsCreateView(BSModalCreateView):
    template_name = 'task_orders/parts_form.html'
    form_class = PartsByTaskForm
    success_message = 'Success: Part was added.'
    task_id = 0

    def dispatch(self, request, *args, **kwargs):
        self.task_id = self.kwargs.get('pk')
        return super(AddPartsCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # check if the part is in the task
        part = form.cleaned_data['part']
        quantity = form.cleaned_data['quantity']
        obj_part = Part.objects.get(part_number=part)
        task = Task.objects.get(pk=self.task_id)

        if obj_part.available < quantity:
            form.add_error(
                'part', 'Incident you do not have enough this part')
            return self.form_invalid(form)

        obj = form.save(commit=False)
        obj.task = task
        obj.operation = 'Add'
        return super(AddPartsCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        url = reverse("work_orders:update_task", kwargs={"pk": self.task_id})
        return url

    def get_context_data(self, **kwargs):
        # Modal title
        context = {
            "task": self.task_id,
            "button": "Add"
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class PartUpdateView(UpdateView):

    model = PartsByTask
    template_name = 'task_orders/parts_form.html'
    form_class = PartsByTaskForm
    success_message = 'Success: Part was updated.'
    obj_part = dict()
    part_id = 0

    def dispatch(self, request, *args, **kwargs):
        self.part_id = self.kwargs.get('pk')
        self.obj_part = Part.objects.get(id=self.part_id)
        return super(PartUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        part = form.cleaned_data['part']
        quantity = form.cleaned_data['quantity']

        obj = form.save(commit=False)
        obj.operation = 'Update'

        if self.obj_part.available < quantity:
            form.add_error(
                'part', 'Incident you do not have enough this part')
            return self.form_invalid(form)
        return super(PartUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Modal title
        context = {
            "part": self.part_id,
            "title": "Edit Part",
            "button": "Update"
        }
        context.update(kwargs)
        return super(PartUpdateView, self).get_context_data(**context)

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        qs = PartsByTask.objects.get(pk=pk)
        url = reverse("work_orders:update_task", kwargs={"pk": qs.task.pk})
        return url


class PartDeleteView(DeleteView):
    model = PartsByTask
    template_name = 'delete_form.html'
    success_message = 'Success: Part was deleted.'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('id')
        url = reverse("work_orders:update_task", kwargs={"pk": pk})
        return url

    def get_context_data(self, **kwargs):
        # Modal title
        context = {
            "message": "Are you sure you want to delete this part",
            "title": "Delete part"
        }
        context.update(kwargs)
        return super(PartDeleteView, self).get_context_data(**context)
