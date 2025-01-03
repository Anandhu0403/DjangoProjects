from django.shortcuts import render,redirect
from books.models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,"home.html")
@login_required
def addbooks(request):
    if(request.method=="POST"):
        title=request.POST['title']
        author=request.POST['author']
        language=request.POST['language']
        pages=request.POST['pages']
        price=request.POST['price']
        cover=request.FILES['cover']
        pdf=request.FILES['pdf']
        b=Book.objects.create(title=title,author=author,language=language,pages=pages,price=price,cover=cover,pdf=pdf) #creates new record
        b.save()#saves record inside table
        return viewbooks(request)
    return render(request,"add.html")
@login_required
def viewbooks(request):
   k=Book.objects.all()
   context={'book':k}
   return render(request,"view.html",context)
@login_required
def detail(request,p):
     k= Book.objects.get(id=p)
     context = {'book':k}
     return render(request,"detail.html",context)
@login_required
def edit(request,p):
    k = Book.objects.get(id=p)
    context = {'book': k}
    if (request.method == "POST"):
        k.title = request.POST['title']
        k.author = request.POST['author']
        k.language = request.POST['language']
        k.pages = request.POST['pages']
        k.price = request.POST['price']
        if(request.FILES.get('cover')==None):
            k.save()
        else:
            k.cover = request.FILES['cover']
        if (request.FILES.get('pdf') == None):
            k.save()
        else:
            k.pdf = request.FILES['pdf']

        # creates new record
        k.save()  # saves record inside table
        return viewbooks(request)
    return render(request,"edit.html",context)
@login_required
def delete(request,p):
    k =Book.objects.get(id=p)
    k.delete()
    return redirect('books:viewbooks')
    return render(request, "delete.html")
from django.db.models import Q
def searchbooks(request):
    b=None
    query=""
    if(request.method=="POST"):
        query=request.POST['search']
        print(query)
        if query:
            b=Book.objects.filter(Q(title__icontains=query)| Q(author__icontains=query)) #django lookups

    return render(request,'search.html',{"book":b,'query':query})