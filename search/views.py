from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from work_orders.models import WorkOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class SearchOrderView(LoginRequiredMixin, ListView):
    template_name = "work_orders/index.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return WorkOrder.objects.search(query)
        return WorkOrder.objects.all()
