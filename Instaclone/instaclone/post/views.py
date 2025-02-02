from django.db import transaction
from django.shortcuts import render,redirect,get_object_or_404,reverse
from post.models import Tag,Follow,Stream,Post,Likes
from userauths.models import Profile
from post.forms import Newpostform
from django.http import HttpResponseRedirect
from comments.models import Comments
from comments.forms import Commentform
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
@login_required
# Create your views here.
def index(request):
    user=request.user
    posts=Stream.objects.filter(user=user)
    all_users=User.objects.all()
    group_ids=[]
    for post in posts:
        group_ids.append(post.post_id)
    post_items=Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context={
        'post_items':post_items,
        'all_users':all_users,
    }

    return render(request,'index.html',context)
def Newpost(request):
    user=request.user.id
    tags_objs=[]
    if(request.method=='POST'):
        form=Newpostform(request.POST,request.FILES)
        if form.is_valid():
            picture=form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tags_list=list(tag_form.split(','))
            for tag in tags_list:
                t,created =Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p,created=Post.objects.get_or_create(picture=picture,caption=caption,user_id=user)
            p.tag.set(tags_objs)
            p.save()
            return redirect('post:index')
    else:
        form=Newpostform()
    context={'form':form}
    return render(request,'newpost.html',context)

def Postdetail(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    # comment
    comments=Comments.objects.filter(post=post).order_by("-date")
    # comment form
    if (request.method == 'POST'):
        form = Commentform(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.user=request.user
            comment.save()
            return HttpResponseRedirect(reverse('post:post_detail', args=[post_id]))
    else:
        form = Commentform()

    context={'post':post,'form': form,
             'comments':comments,
      }
    return render(request,'post_details.html',context)

def Like(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    current_likes=post.likes
    liked=Likes.objects.filter(user=user,post=post).count()
    if not liked:
        liked=Likes.objects.create(user=user,post=post)
        current_likes += 1
    else:
        liked=Likes.objects.filter(user=user,post=post).delete()
        current_likes -= 1
    post.likes=current_likes
    post.save()
    return HttpResponseRedirect(reverse('post:post_detail',args=[post_id]))

def Tags(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    posts=Post.objects.filter(tag=tag).order_by('-posted')
    context={'tag':tag,'posts':posts}
    return render(request,'tags.html',context)

def favorite(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    profile=Profile.objects.get(user=user)
    if profile.favorite.filter(id=post_id).exists():
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)
    return HttpResponseRedirect(reverse('post:post_detail',args=[post_id]))

def delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    context={'post':post}

    # Check if the current user is the owner of the post
    if post.user_id != request.user.id:
        return redirect('post:index')  # Redirect if unauthorized

    if request.method == 'POST':
        post.delete()
        return redirect('post:index')
    return render(request,'deletepost.html',context)

