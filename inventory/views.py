from django.http import JsonResponse
from django.shortcuts import render
from .models import Part
from work_orders.models import Task, PartsByTask


def get_price_api(request):
    obj = Part.objects.get(pk=request.GET.get("id"))
    task = Task.objects.get(pk=request.GET.get("task"))
  
    part_exist_in_task = valid_part_exist_in_task(obj,task)


    if obj:
        part_data = {
            "price": obj.price,
            "available": obj.available,
            "part_exist_in_task": part_exist_in_task,
        }
    return JsonResponse(part_data)


def valid_part_exist_in_task(obj, task):
    parts_by_task = PartsByTask.objects.filter(task=task, part = obj)

    if parts_by_task:
        return ("yes")
    else:
        return ("no")
