
from django.forms import ModelForm, TextInput, Select
from .models import WorkOrder


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


#<input class="form-control" type="text" placeholder="Readonly input here…" readonly>
