from django.urls import path
from django.contrib.auth.views import (
    LogoutView
)


app_name = 'account'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
