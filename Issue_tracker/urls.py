"""Issue_tracker URL Configuration

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
from django.contrib import admin
from django.urls import path
from api.sys_access import UserMgt, UserLogin
from api.views import ProjectList, ClientList, IssuesList, IssueAction, GetStatusCount, ProjectClient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserMgt.as_view()),
    path('login/', UserLogin.as_view()),

    path('clients/', ClientList.as_view()),
    path('projects/', ProjectList.as_view()),
    path('project-client/', ProjectClient.as_view()),
    path('issues/', IssuesList.as_view()),
    path('issue-action/', IssueAction.as_view()),
    path('status-count/', GetStatusCount.as_view()),


]
