from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def register(request):
    if(request.method=="POST"):
        username=request.POST['username']
        password=request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        firstname= request.POST['firstname']
        lastname= request.POST['lastname']
        if(password==confirmpassword):
            u=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname)
        else:
            return HttpResponse("Passwords are not same")
        return redirect('users:login')
    return render(request,'register.html')

def userlogin(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('shop:category')
        else:
            return HttpResponse('Invalid username or password')
    return  render(request,'login.html')

def userlogout(request):
    logout(request)
    return redirect('shop:category')