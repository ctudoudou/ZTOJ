"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('contests/', contests, name='contests'),
    path('ranklist/', ranklist, name='ranklist'),
    path('problems/', problems, name='problems'),
    path('login/', do_login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('rankist/', rankist, name='rankist'),
    path('contest/', contest, name='contest'),
    path('contest/<cn>', contest, name='contest'),
    path('contestrank/<cn>', contest_rank, name='contestrank'),
    path('contestrank/', contest_rank, name='contestrank'),
    path('problem/<id>', problem, name='problem'),
    path('problem/', problem, name='problem'),
    path('mypage/', personal,name='personal'),
    path('reogin/', register_login, name='register_login'),
    path('profile/', profile, name='profile'),
    path('api/goal/<token>', api_goal, name='adp_goal')
]
