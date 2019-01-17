
from django.forms import ModelForm, TextInput, Select, Textarea
from .models import WorkOrder, Task, PartsByTask
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            'number_order',
            'client',
            'truck',
        ]
        widgets = {
            "number_order": TextInput(attrs={"class": "form-control", "type": "text", "readonly": True}),
            "client": Select(attrs={"class": "form-control"}),
            "truck": Select(attrs={"class": "form-control"})
        }


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            "work_order",
            "title",
            "description",
            "time_labor",
            "mechanic",
        ]
        widgets = {
            "work_order": TextInput(attrs={"class": "form-control", "type": "text", "readonly": True}),
            "title": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "time_labor": TextInput(attrs={"class": "form-control"}),
            "mechanic": Select(attrs={"class": "form-control"}),
        }

class PartsByTaskForm(PopRequestMixin, CreateUpdateAjaxMixin, ModelForm):
    class Meta:
        model = PartsByTask
        exclude = [
            'task',
            'subtotal',
        ]