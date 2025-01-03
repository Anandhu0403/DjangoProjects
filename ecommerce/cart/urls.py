"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from cart import views
app_name="cart"
urlpatterns = [
    path('<int:p>',views.cart,name="usercart"),
    path('cart/',views.cartview,name="cartview"),
    path('cart_remove/<int:p>',views.cartremove,name="cartremove"),
    path('cartdelete/<int:p>',views.cartdelete,name="cartdelete"),
    path('checkout/',views.checkout,name="checkout"),
    path('paymentstatus/<p>',views.payment_status,name="paymentstatus"),
    path('yourorders/',views.yourorders,name="yourorders"),

]
