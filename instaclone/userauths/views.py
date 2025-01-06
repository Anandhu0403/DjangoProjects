from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from post.models import Post,Follow,Stream
from userauths.models import Profile
from userauths.forms import EditProfileForm
from django.core.paginator import Paginator
from userauths.forms import UserRegisterForm

from django.contrib import messages
# Create your views here.
def Userprofile(request,username):
    user=get_object_or_404(User,username=username)
    profile=Profile.objects.get(user=user)
    url_name=resolve(request.path).url_name
    if url_name == 'profile':
        posts=Post.objects.filter(user=user).order_by('-posted')
    else:
        posts=profile.favorite.all()

    #track following
    post_count=Post.objects.filter(user=user).count()
    following_count=Follow.objects.filter(follower=user).count()
    follow_count=Follow.objects.filter(following=user).count()
    #follow status
    follow_status=Follow.objects.filter(following=user,follower=request.user).exists()

    #pagination
    paginator=Paginator(posts,3)
    page_number=request.GET.get('page')
    posts_paginator=paginator.get_page(page_number)

    context = {
        'post_paginator': posts_paginator,
        'profile':profile,
        'posts':posts,
        'post_count':post_count,
        'following_count':following_count,
        'follow_count':follow_count,
        'follow_status':follow_status,
    }

    return render(request, 'profile.html', context)

def follow(request,username,option):
    user=request.user
    following=get_object_or_404(User,username=username)
    try:
        f,created=Follow.objects.get_or_create(follower=user,following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following,user=user).all().delete()
        else:
            posts=Post.objects.filter(user=following)[:10]
            with transaction.atomic():
                for post in posts:
                    stream=Stream(post=post,user=user,date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile',args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile',args=[username]))

def editprofile(request):
    user=request.user.id
    profile=Profile.objects.get(user__id=user)
    if request.method=="POST":
        form=EditProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile.picture=form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.bio = form.cleaned_data.get('bio')
            profile.location = form.cleaned_data.get('location')
            #profile.url = form.cleaned_data.get('url')
            profile.save()
            return redirect('profile',profile.user.username)
    else:
            form=EditProfileForm()

    context = {
        'form': form, }

    return render(request, 'edit_profile.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray {username} your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'], )
            login(request, new_user)

            return redirect('editprofile')



    elif request.user.is_authenticated:
        return redirect('post:index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('sign-in')