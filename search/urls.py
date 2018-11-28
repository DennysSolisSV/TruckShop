from django.conf.urls import url
from .views import SearchOrderView

app_name = 'search'

urlpatterns = [
    url(r'^order/$', SearchOrderView.as_view(), name='query'),
]
