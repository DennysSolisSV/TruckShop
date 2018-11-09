from django.conf.urls import url
from django.contrib import admin

from .views import (
	   MainView, clock_in, clock_out
	)
app_name =  'work_orders'

urlpatterns = [
	url(r'^$', MainView.as_view(), name='index'),
    url(r'^clockin/$', clock_in, name='clockin'),
    url(r'^clockout/$', clock_out, name='clockout'),
]
