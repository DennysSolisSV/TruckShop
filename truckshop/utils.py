

def unique_work_order_number_generator(instance):
    Klass = instance.__class__
    order_number = Klass.objects.latest('number_order')
    if order_number:
        order_new_number = int(order_number.number_order) + 1
    return order_new_number
