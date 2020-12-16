from django.forms import ModelForm, TextInput, Select, Textarea
from .models import WorkOrder, Task, PartsByTask
from truck.models import Truck


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            'number_order',
            'client',
            'truck',
            'total_parts',
            'total_labor',
            'total_work_order',
            "status",
        ]
        widgets = {
            "number_order": TextInput(attrs={
                "class": "form-control", "type": "text", "readonly": True
            }),
            "client": Select(attrs={"class": "form-control"}),
            "truck": Select(attrs={"class": "form-control"}),
            "status": Select(attrs={"class": "form-control"}),
            "total_parts": TextInput(attrs={"class": "form-control", "readonly": True}),
            "total_labor": TextInput(attrs={"class": "form-control", "readonly": True}),
            "total_work_order": TextInput(attrs={"class": "form-control", "readonly": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['truck'].queryset = Truck.objects.none()

        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['truck'].queryset = Truck.objects.filter(
                    client_id=client_id).order_by('fleet')
            except (ValueError, TypeError):
                pass  # invalid input from the client;
                # ignore and fallback to empty Truck queryset
        elif self.instance.pk:
            self.fields['truck'].queryset = self.instance.client.truck_set.order_by(
                'fleet')


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = [
            "work_order",
            "title",
            "description",
            "time_labor",
            "mechanic",
            "status",
            "total_parts",
            "total_labor",
            "total_task"
        ]
        widgets = {
            "work_order": TextInput(attrs={
                "class": "form-control", "type": "text", "readonly": True
            }),
            "title": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "time_labor": TextInput(attrs={
                'class': 'form-control', 'autocomplete': 'off', 
                "placeholder": "0", 
                "oninput": "this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');" 
            }),
            "mechanic": Select(attrs={"class": "form-control"}),
            "status": Select(attrs={"class": "form-control"}),
            "total_parts": TextInput(attrs={"class": "form-control", "readonly": True}),
            "total_labor": TextInput(attrs={"class": "form-control", "readonly": True}),
            "total_task": TextInput(attrs={"class": "form-control", "readonly": True}),
        }


class PartsByTaskForm(ModelForm):
    class Meta:
        model = PartsByTask
        exclude = [
            'task',
            'price',
            'subtotal',
            'operation'
        ]
        widgets = {
            "part": Select(attrs={"class": "form-control part_task_select", "id": "parttaskselect"}),
            # use oninput to allow only numeric
            "quantity": TextInput(attrs={"class": "form-control", "autocomplete": "off", 
                "placeholder": "0", "oninput": "this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');" 
            }),

        }
