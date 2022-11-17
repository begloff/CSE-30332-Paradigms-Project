from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Candidate, Recruiter

def index(request):
    return HttpResponse("Hello, world!")

class AccountView(DetailView):
    model = Candidate
    template_name = 'account.html'

class RecruitView(DetailView):
    model = Recruiter
    template_name = 'recaccount.html'

   