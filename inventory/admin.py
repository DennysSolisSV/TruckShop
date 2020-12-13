from django.contrib import admin

from .models import Part

class PartAdmin(admin.ModelAdmin):
    list_display = ['part_number', 'price', 'cost', 
        'existence', 'available',
    ]

admin.site.register(Part, PartAdmin) 
