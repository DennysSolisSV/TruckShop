from django.http import JsonResponse
from django.shortcuts import render
from .models import Part


def get_price_api(request):
    obj = Part.objects.get(pk=request.GET.get("id"))
    if obj:
        part_data = {
            "price": obj.price,
            "existence": obj.existence
        }
    else:
        part_data = {
            "price": "0.00",
            "existence": "0"
        }
    return JsonResponse(part_data)
