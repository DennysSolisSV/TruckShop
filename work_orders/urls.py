from django.conf.urls import url

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
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^ajax/load/trucks/$', load_trucks, name='ajax_load_trucks'),
    url(r'^create/$', WorkOrderCreateView.as_view(), name='create'),
    url(r'^clockin/$', clock_in, name='clockin'),
    url(r'^clockout/$', clock_out, name='clockout'),
    url(r'^start/$', start_or_end_task, name='start_or_end'),
    url(r'^timecard/$', TimeCardView.as_view(), name='time_card'),
    url(r'^order/(?P<slug>[\w-]+)/$',
        WorkOrderUpdateView.as_view(), name='detail'),
    url(r'^task/(?P<pk>\d+)/$',
        TaskUpdateView.as_view(), name='update_task'),
    url(r'^task/delete/(?P<pk>\d+)/$',
        TaskDeleteView.as_view(), name='delete_task'),
    # url(r'^task/save/(?P<pk>\d+)/$',
    #     TaskUpdateView.as_view(), name='update_task'),
    url(r'^update/timelabor/$',
        task_time_labor_update_api, name='update_task_time_labor_ajax'),
    url(r'^order/task/used/part/(?P<pk>\d+)/$',
        AddPartsCreateView.as_view(), name='add_part'),
    url(r'^order/task/update/part/(?P<pk>\d+)/$',
        PartUpdateView.as_view(), name='update_part'),
    url(r'^order/task/delete/part/(?P<pk>\d+)/(?P<id>\d+)/$',
        PartDeleteView.as_view(), name='delete_part'),

]
