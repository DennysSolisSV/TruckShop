from django.conf.urls import url

from .views import (
    get_price_api,
)

app_name = 'inventory'

urlpatterns = [
    url(r'^price/$', get_price_api, name='part_price'),
]
