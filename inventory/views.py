from django.http import JsonResponse
from django.shortcuts import render
from .models import Part
from work_orders.models import Task, PartsByTask


def get_price_api(request):
    obj = Part.objects.get(pk=request.GET.get("id"))
    task = Task.objects.get(pk=request.GET.get("task"))
  
    part_exist_in_task, quantity = valid_part_exist_in_task(obj,task)
    print(quantity)

    if obj:
        part_data = {
            "price": obj.price,
            "available": obj.available,
            "part_exist_in_task": part_exist_in_task,
            "quantity": quantity,
        }
    return JsonResponse(part_data)


def valid_part_exist_in_task(obj, task):
    parts = PartsByTask.objects.get(task=task, part = obj)

    if parts:
        return ("yes", parts.quantity)
    else:
        return ("no", 0)
