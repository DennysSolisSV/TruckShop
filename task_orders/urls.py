from django.conf.urls import url

from .views import (
    TaskCreateView,
)

app_name = 'task_orders'

urlpatterns = [
    url(r'^create/$', TaskCreateView.as_view(), name='create'),
]