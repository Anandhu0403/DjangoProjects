"""
URL configuration for instaclone project.

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
from django.contrib import admin
from django.urls import path
from post import views
app_name="post"
urlpatterns = [
    path('',views.index,name="index"),
    path('newpost/',views.Newpost,name="newpost"),
    path('<uuid:post_id>/',views.Postdetail,name="post_detail"),
    path('<uuid:post_id>/like',views.Like,name="like"),
    path('tag/<slug:tag_slug>/',views.Tags,name="tags"),
    path('<uuid:post_id>/favorite',views.favorite,name="favorite"),
]
