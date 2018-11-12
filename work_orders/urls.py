from django.conf.urls import url

from .views import (
    MainView, TimeCardView, WorkOrderView, clock_in, clock_out
)
app_name = 'work_orders'

urlpatterns = [
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^clockin/$', clock_in, name='clockin'),
    url(r'^clockout/$', clock_out, name='clockout'),
    url(r'^timecard/$', TimeCardView.as_view(), name='time_card'),
    url(r'^order/$', WorkOrderView.as_view(), name='order'),

]
