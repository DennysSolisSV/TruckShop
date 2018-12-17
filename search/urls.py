from django.conf.urls import url
from .views import SearchOrderView

app_name = 'search'

urlpatterns = [
    url(r'^$', SearchOrderView.as_view(), name='query'),
]
