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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from userauths.models import Profile
from userauths.views import Userprofile,follow
from direct.views import direct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('post.urls')),
    path('users/', include('userauths.urls')),
    #path('users/',include('comments.urls')),
    path('message/',include('direct.urls')),
    # profile section
    path('<username>/',Userprofile,name="profile"),
    path('<username>/saved',Userprofile,name="favorite"),
    path('<username>/follow/<option>', follow, name="follow"),

    #mesage section



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)