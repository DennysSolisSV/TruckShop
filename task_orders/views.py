from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView,
    DeleteView
)


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
            "task_pk": 1,
        }

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url(self, **kwargs):
        work_order = WorkOrder.objects.get(
            id=self.request.session.get("work_order_id", None))
        urls = reverse("work_orders:detail", kwargs={
            "slug": work_order.slug})
        return urls


class TaskUpdateView(UpdateView):
    template_name = 'task_orders/task_detail.html'
    queryset = Task.objects.all()
    form_class = TaskForm

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
            "task_pk": self.kwargs.get('pk'),
        }

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url(self, **kwargs):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        url = reverse("work_orders:detail", kwargs={
                      "slug": task.work_order.slug})
        return url


class TaskDeleteView(DeleteAjaxMixin, DeleteView):
    model = Task
    template_name = 'task_orders/delete_task_form.html'
    success_message = 'Success: Task was deleted.'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('id')
        url = reverse("work_orders:update_task", kwargs={"pk": pk})
        return url


class AddPartsCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'task_orders/parts_form.html'
    form_class = PartsByTaskForm
    success_message = 'Success: Part was added.'

    def form_valid(self, form):
        # check if the part is in the task
        part = form.cleaned_data['part']
        quantity = form.cleaned_data['quantity']
        obj_part = Part.objects.get(part_number=part)
        task = Task.objects.get(pk=self.kwargs.get('pk'))

        qs = PartsByTask.objects.filter(task_id=task.id, part_id=part)
        if qs.exists():
            form.add_error(
                'part', 'Incident with this part already in this task.')
            return self.form_invalid(form)

        if obj_part.available < quantity:
            form.add_error(
                'part', 'Incident you do not have enough this part')
            return self.form_invalid(form)

        obj = form.save(commit=False)
        obj.task = task
        obj.operation = 'Add'
        return super(AddPartsCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        url = reverse("work_orders:update_task", kwargs={"pk": pk})
        return url

    def get_context_data(self, **kwargs):
        # Modal title
        context = {
            "title": "Add Part",
            "button": "Add"
        }
        context.update(kwargs)
        return super(AddPartsCreateView, self).get_context_data(**context)


class PartUpdateView(PassRequestMixin, SuccessMessageMixin,
                     UpdateView):

    model = PartsByTask
    template_name = 'task_orders/parts_form.html'
    form_class = PartsByTaskForm
    success_message = 'Success: Part was updated.'

    def form_valid(self, form):
        part = form.cleaned_data['part']
        obj_part = Part.objects.get(part_number=part)
        quantity = form.cleaned_data['quantity']

        obj = form.save(commit=False)
        obj.operation = 'Update'

        if obj_part.available < quantity:
            form.add_error(
                'part', 'Incident you do not have enough this part')
            return self.form_invalid(form)
        return super(PartUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Modal title
        context = {
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


class PartDeleteView(DeleteAjaxMixin, DeleteView):
    model = PartsByTask
    template_name = 'task_orders/delete_part_form.html'
    success_message = 'Success: Part was deleted.'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('id')
        url = reverse("work_orders:update_task", kwargs={"pk": pk})
        return url
