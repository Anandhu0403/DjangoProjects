from django.contrib import admin
from cart.models import Cart,Payment,Orderdetails
# Register your models here.
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Orderdetails)