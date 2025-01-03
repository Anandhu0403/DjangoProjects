from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Category,Products
# Create your views here.
def home(request):
    return render(request,'home.html')
def category(request):
    k=Category.objects.all()
    context={"category":k}
    return render(request,'categories.html',context)

def products(request,p):
    k=Category.objects.get(id=p)
    c=Products.objects.filter(category=k)
    context={'category':k,'products':c,}
    return render(request,'product.html',context)

def productdetail(request,p):
    k=Products.objects.get(id=p)
    context={'detail':k}
    return render(request,'detail.html',context)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def addcategories(request):
    if(request.method == "POST"):
        name=request.POST['name']
        desc=request.POST['desc']
        image=request.FILES['image']
        b=Category.objects.create(name=name,desc=desc,image=image)
        b.save()
    return render(request,'addcategories.html')

def addproduct(request):

    if (request.method == "POST"):
        name = request.POST['name']
        desc = request.POST['desc']
        image = request.FILES['image']
        price = request.POST['price']
        stock = request.POST['stock']
        category_id=request.POST.get('category')
        category=get_object_or_404(Category,id=category_id)
        b = Products.objects.create(name=name, desc=desc, image=image,price=price,stock=stock,category=category)
        b.save()
    return render(request,'addproduct.html')

def addstock(request,p):
    k = Products.objects.get(id=p)
    context = {'detail': k}
    if(request.method=="POST"):
        k.stock=request.POST['stock']
        k.save()
        return redirect('shop:productdetail',p)
    return render(request,'addstock.html',context)