from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from direct.models import Message
from django.core.paginator import Paginator

@login_required
def inbox(request):
    user=request.user
    messages=Message.get_message(user=user)
    active_direct=None
    directs=None
    if messages:
        message=messages[0]
        active_direct=message['user'].username
        directs=Message.objects.filter(user=user,recipient=message['user'])
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == active_direct:
                message['unread']=0
    context={
            'directs':directs,
            'active_direct':active_direct,
            'messages':messages,
        }
    return render(request,'direct/inbox.html',context)


def direct(request, username):
    user = request.user
    # Get list of users with messages
    messages = Message.get_message(user=user)

    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username).order_by('date')

    # Mark messages as read
    directs.update(is_read=True)

    # Set unread count to 0 for the active user
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
    }
    return render(request, 'direct/directs.html', context)

def Sendmesage(request):
    from_user=request.user
    to_user_username=request.POST.get('to_user')
    body=request.POST.get('body')
    if request.method== 'POST':
        to_user=User.objects.get(username=to_user_username)
        Message.send_message(from_user,to_user,body)
        return redirect('inbox')
    else:
        pass

def Usersearch(request):
    query=request.GET.get('q')
    context={}
    if query:
        users=User.objects.filter(Q(username__icontains=query)|Q(profile__first_name__icontains=query) |
            Q(profile__last_name__icontains=query))

        #paginator
        paginator = Paginator(users,8)
        page_number=request.GET.get('page')
        users_paginator=paginator.get_page(page_number)
        context = {
            'users': users_paginator,

        }
    return render(request, 'direct/search.html', context)

def Newmesage(request,username):
    from_user=request.user
    body=''
    try:
        to_user=User.objects.get(username=username)
    except Exception as e:
        return redirect('user-search')

    if from_user !=to_user:
        Message.send_message(from_user,to_user,body)
    return redirect('inbox')