from django.urls import path

from .views import (
    TaskCreateView,
)

app_name = 'task_orders'

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='create'),
    
]