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
from shop import views
app_name="shop"
urlpatterns = [
    path('',views.category,name="category"),
    # path('categories',views.category,name="category"),
    path('products/<int:p>',views.products,name='products'),
    path('productdetail/<int:p>',views.productdetail,name="productdetail"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('addcategories',views.addcategories,name="addcategories"),
    path('addproduct',views.addproduct,name="addproduct"),
    path('addstock/<int:p>',views.addstock,name="addstock"),

]
