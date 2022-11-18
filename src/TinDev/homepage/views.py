from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Candidate, Recruiter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from .forms import CandidateForm

def index(request):
    return HttpResponse("Hello, world!")

class AccountView(DetailView):
    model = Candidate
    template_name = 'account.html'

class RecruitView(DetailView):
    model = Recruiter
    template_name = 'recaccount.html'

def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new = form.save()
            new = authenticate( username = form.cleaned_data['username'], password = form.cleaned_data['password1'],)
            login(request,new)
            return HttpResponseRedirect('/homepage/accounts/profile/')


    context = {'form': form}
    return render(request, 'register.html', context)

def profileRegistration(request):
    form = CandidateForm()

    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/homepage/')
    context = {'form': form}
    return render(request, 'profile.html', context)