from django.contrib import admin

# Register your models here.

from .models import WorkOrder, Task, PartsByTask, MechachicTimeTask

class WorkOrderAdmin(admin.ModelAdmin):
    readonly_fields = ['number_order',]


admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Task)
admin.site.register(PartsByTask)
admin.site.register(MechachicTimeTask)
