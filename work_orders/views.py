from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import Group


class MainView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # verify that the user is mechanic
        user = request.user

        if check_group(user, 'Employees'):
            template = 'index.html'
        elif check_group(user, 'Mechanics'):
            template = 'work_orders/index2.html'
        else:
            template = 'work_orders/index3.html'

        return render(request, template)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MainView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['publisher'] = '1'
        print(context)
        return context


def clock_in(request):
    return redirect('work_orders:index')


def clock_out(request):
    return redirect('work_orders:index')


def check_group(user, name_group):
    if user.groups.filter(name=name_group).exists():
        return True
    else:
        return False
