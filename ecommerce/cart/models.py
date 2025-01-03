from django.db import models
from shop.models import Products
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    dateadded=models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.name


class Orderdetails(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.BigIntegerField()
    pin=models.IntegerField()
    no_of_items=models.IntegerField()
    orderid=models.CharField(max_length=30)
    paymentstatus=models.CharField(max_length=30,default="pending")
    deliverystatus=models.CharField(max_length=30,default="pending")
    orderdate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
class Payment(models.Model):
    name=models.CharField(max_length=30)
    amount=models.IntegerField()
    orderid=models.CharField(max_length=30)
    razorpay_id=models.CharField(max_length=30,blank=True)
    paid=models.BooleanField(default=False)
    def __str__(self):
        return self.orderid