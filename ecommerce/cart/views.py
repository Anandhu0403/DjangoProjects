from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart,Payment,Orderdetails
from shop.models import Products
import  razorpay
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required
def cart(request,p):
    c=Products.objects.get(id=p)
    u=request.user   #inbuilt django feature to know the user details
    try:
        v=Cart.objects.get(user=u,product=c)   #alredy object exists in that case increment quantity only
        v.quantity+=1
        c.stock-=1
        c.save()
        v.save()
    except:
        v=Cart.objects.create(product=c,user=u,quantity=1)  # if product does not exists then create new object for this specific user
        c.stock-=1
        c.save()
        v.save()
    return redirect('cart:cartview')
@login_required()
def cartview(request):
    u=request.user
    c=Cart.objects.filter(user=u)
    total=0
    for i in c:
        total+=i.quantity*i.product.price
    context={'cart':c,'user':u,'total':total}
    return render(request,'usercart.html',context)

def cartremove(request,p):
    u=request.user
    x=Products.objects.get(id=p)
    c=Cart.objects.get(user=u,product=x)
    if(c.quantity > 1):
        c.quantity -=1
        c.save()
        x.stock += 1
        x.save()
    else:
        c.delete()
        x.stock += 1
        x.save()
    return redirect('cart:cartview')
def cartdelete(request,p):
    u=request.user
    x=Products.objects.get(id=p)
    try:
        c = Cart.objects.get(user=u, product=x)
        quantity=c.quantity
        c.delete()

        x.stock += quantity
        x.save()
    except:
        pass
    return redirect('cart:cartview')

def checkout(request):
    if(request.method=="POST"):
        pincode=request.POST['pincode']
        address=request.POST['address']
        phonenumber=request.POST['phonenumber']
        u=request.user
        total = 0
        c=Cart.objects.filter(user=u)

        for i in c:
            total+=i.product.price*i.quantity
        print(total)
        # razorpay connection
        client=razorpay.Client(auth=('rzp_test_Da0XLdCEyEjFiQ','gAv50WyYWfnb9lGroE9AtQTu'))
        #razorpay order creation
        response_payment=client.order.create(dict(amount=int(total*100),currency='INR'))
        order_id=response_payment['id']
        status=response_payment['status']
        if(status=='created'):
            p=Payment.objects.create(name=u.username,amount=total,orderid=order_id)
            p.save()
            for i in c:
                o=Orderdetails.objects.create(product=i.product,user=i.user,phone=phonenumber,address=address,pin=pincode,orderid=order_id,no_of_items=i.quantity)
                o.save()
            context={'payment':response_payment,'name':u.username}

            return render(request, 'payment.html',context)



    return render(request,'checkout.html')
@csrf_exempt

def payment_status(request,p):
    user=User.objects.get(username=p)
    login(request,user)
    response=request.POST #razorpay response after payment
    print(response)
    # To Check the validity(authenticity) of razorpay payment details received by application
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],
    }

    client=razorpay.Client(auth=('rzp_test_Da0XLdCEyEjFiQ','gAv50WyYWfnb9lGroE9AtQTu'))
    try:
        status=client.utility.verify_payment_signature(param_dict)      #for checking the payment details
                                                                        # we pass param_dict to verify_payment_signature function
        print(status)
        p=Payment.objects.get(orderid=response['razorpay_order_id']) #after sucess payment record in payment model matching with order_id
        p.razorpay_id=response['razorpay_payment_id']
        p.paid=True
        p.save()

        o=Orderdetails.objects.filter(orderid=response['razorpay_order_id'])
        for i in o:
            i.paymentstatus="completed"
            i.save()
        # to remove cart items after payment
        c=Cart.objects.filter(user=user)
        c.delete()
    except:
        pass

    return render(request,'paymentstatus.html')

def yourorders(request):
    u=request.user
    o=Orderdetails.objects.filter(user=u,paymentstatus="completed")
    context={'orders':o}
    return render(request,'yourorders.html',context)