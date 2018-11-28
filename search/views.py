from django.views.generic import ListView
from work_orders.models import WorkOrder


class SearchOrderView(ListView):
    template_name = "work_orders/index.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return WorkOrder.objects.search(query)
        return WorkOrder.objects.all()
