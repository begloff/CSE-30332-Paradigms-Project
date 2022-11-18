from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import logout

from . import views
app_name = 'homepage'  # creates a namespace for this app
urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('info/<int:pk>', views.AccountView.as_view()),
    path('recinfo/<int:pk>', views.RecruitView.as_view()),
    path('accounts/register/', views.registerPage),
    path('accounts/profile/', views.profileRegistration)
]
