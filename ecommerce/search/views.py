from django.db.models import Q
from django.shortcuts import render
from shop.models import Products,Category
# Create your views here.
def searchproduct(request):
    b=None
    query=""
    if(request.method=="GET"):
        query=request.GET['search']
        if (query):
            b=Products.objects.filter(Q(name__icontains=query)| Q(desc__icontains=query))
    return render(request, 'search.html', {"products":b, 'query': query})
