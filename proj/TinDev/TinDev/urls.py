"""TinDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import logout

from users.views import PostUpdateView, PostDeleteView, PostIndexViewAll, PostIndexViewActive, PostIndexViewInactive, CandidateSignUpView, RecruiterSignUpView, home, CreatePostView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', home, name="home"),
    path('accounts/signup/candidate', CandidateSignUpView.as_view(), name='candidate_signup'),
    path('accounts/signup/recruiter', RecruiterSignUpView.as_view(), name='recruiter_signup'),
    path('post/create', CreatePostView.as_view(), name='post_create'),
    path('post/view/all', PostIndexViewAll.as_view(), name='post_view_all'),
    path('post/view/active', PostIndexViewActive.as_view(), name='post_view_active'),
    path('post/view/inactive', PostIndexViewInactive.as_view(), name='post_view_inactive'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
