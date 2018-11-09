

from accounts.forms import LoginForm
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import(
    LoginView,
    )

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/', include("work_orders.urls")),
    url(r'^$', LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login')
]
