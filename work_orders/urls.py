from django.conf.urls import url

from .views import (
    MainView, TimeCardView, clock_in,
    clock_out, start_or_end_task,
    WorkOrderdetailView, WorkOrderCreateView, TaskDetailView, AddPartsCreateView,
)

app_name = 'work_orders'

urlpatterns = [
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^create/$', WorkOrderCreateView.as_view(), name='create'),
    url(r'^clockin/$', clock_in, name='clockin'),
    url(r'^clockout/$', clock_out, name='clockout'),
    url(r'^start/$', start_or_end_task, name='start_or_end'),
    url(r'^timecard/$', TimeCardView.as_view(), name='time_card'),
    url(r'^order/(?P<slug>[\w-]+)/$',
        WorkOrderdetailView.as_view(), name='detail'),
    url(r'^task/(?P<pk>\d+)/$',
        TaskDetailView.as_view(), name='task_detail'),
    url(r'^order/task/used/parts/(?P<pk>\d+)/$', AddPartsCreateView.as_view(), name='add_part'),

]
