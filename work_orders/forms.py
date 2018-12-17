
from django.forms import ModelForm, TextInput
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
            'number_order': TextInput(attrs={'readonly': True})
        }
