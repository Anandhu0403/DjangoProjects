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
from direct import views
urlpatterns = [
    path('inbox/',views.inbox,name="inbox"),
    path('directs/<username>', views.direct, name="direct"),
    path('send/',views.Sendmesage,name="send_message"),
    path('new/',views.Usersearch,name="user-search"),
    path('new/<username>',views.Newmesage,name="new-message"),

]
