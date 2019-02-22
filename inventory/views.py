from django.http import JsonResponse
from django.shortcuts import render
from .models import Part


def get_price_api(request):
    obj = Part.objects.get(pk=request.GET.get("id"))
    if obj:
        part_data = {
            "price": obj.price,
            "available": obj.available
        }
    return JsonResponse(part_data)
