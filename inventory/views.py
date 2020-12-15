from django.http import JsonResponse
from django.shortcuts import render
from .models import Part
from work_orders.models import Task, PartsByTask


def get_price_api(request):
    obj = Part.objects.get(pk=request.GET.get("id"))
    task = Task.objects.get(pk=request.GET.get("task"))
    partbytask = request.GET.get("partbytask")
  
    part_exist_in_task = valid_part_exist_in_task(obj,task, partbytask)
    quantity =  get_available(obj,task, partbytask)
    

    if obj:
        part_data = {
            "price": obj.price,
            "available": obj.available,
            "part_exist_in_task": part_exist_in_task,
            "quantity": quantity,
        }
    return JsonResponse(part_data)


def valid_part_exist_in_task(obj, task, partbytask=0):
    # check if the part exist in the task and it has to be different to the one we updating.
    
    parts = PartsByTask.objects.filter(task=task, part=obj).exclude(pk=partbytask).first()

    if parts:
        exist = "yes"
    else:
        exist = "no"

    return (exist)

def get_available(obj, task, partbytask=None):

    # When update get quantity was saved before to calculate parts available.
    if partbytask:
        parts = PartsByTask.objects.get(pk=partbytask)
        available = parts.quantity
    else:
        available =  0

    return (available)
