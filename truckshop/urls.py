

from accounts.forms import LoginForm
from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.contrib.auth.views import(
    LoginView,
    )

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/', include("search.urls")),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login')
]
