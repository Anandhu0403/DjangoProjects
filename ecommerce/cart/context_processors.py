from cart.models import Cart

def countitem(request):
    count = 0
    if request.user.is_authenticated:
        u = request.user
        c = Cart.objects.filter(user=u)

        for i in c:
            count += i.quantity

    return {'count':count}
