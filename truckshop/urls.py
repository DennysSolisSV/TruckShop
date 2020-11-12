from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView
)

from accounts.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include("work_orders.urls")),
    path('main/order/', include("search.urls")),
    path('main/task/', include("task_orders.urls")),
    path('main/parts/', include("inventory.urls")),
    path('account/', include("accounts.urls")),
    path('', LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=LoginForm), name='login'
    ),
]
