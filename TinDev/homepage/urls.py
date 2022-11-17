from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views
app_name = 'homepage'  # creates a namespace for this app
urlpatterns = [
    #path('', views.index, name='index'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
7