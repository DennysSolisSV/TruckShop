from django.urls import path

from .views import (
    MainView, TimeCardView, clock_in,
    clock_out, start_or_end_task,
    WorkOrderUpdateView, WorkOrderCreateView,
    task_time_labor_update_api, load_trucks
)

from task_orders.views import (
    TaskUpdateView, TaskDeleteView, AddPartsCreateView,
    PartUpdateView, PartDeleteView,
)

app_name = 'work_orders'

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('ajax/load/trucks/', load_trucks, name='ajax_load_trucks'),
    path('create/', WorkOrderCreateView.as_view(), name='create'),
    path('clockin/', clock_in, name='clockin'),
    path('clockout/', clock_out, name='clockout'),
    path('start/', start_or_end_task, name='start_or_end'),
    path('timecard/', TimeCardView.as_view(), name='time_card'),
    path('order/<slug:slug>/', WorkOrderUpdateView.as_view(), name='detail'),
    path('task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('update/timelabor/', task_time_labor_update_api, name='update_task_time_labor_ajax'),
    path('order/task/<int:pk>/add/part/', AddPartsCreateView.as_view(), name='add_part'),
    path('update/part/<int:pk>/', PartUpdateView.as_view(), name='update_part'),
    path('delete/part/<int:pk>/<int:id>/', PartDeleteView.as_view(), name='delete_part'),
]