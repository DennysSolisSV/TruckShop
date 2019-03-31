

def unique_work_order_number_generator(instance):
    if instance:
        Klass = instance.__class__
        order_number = Klass.objects.all()

    if order_number:
        order_number = Klass.objects.latest('number_order')
        order_new_number = int(order_number.number_order) + 1
    else:
        order_new_number = 1
    return order_new_number
