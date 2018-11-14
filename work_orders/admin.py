from django.contrib import admin

# Register your models here.

from .models import WorkOrder, Task, PartsByTask, MechachicTimeTask


admin.site.register(WorkOrder)
admin.site.register(Task)
admin.site.register(PartsByTask)
admin.site.register(MechachicTimeTask)
