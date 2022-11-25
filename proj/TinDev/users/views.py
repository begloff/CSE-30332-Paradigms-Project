from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User
from .forms import CandidateSignUpForm
from django.contrib.auth import login

# Create your views here.

class CandidateSignUpView(CreateView):
    model = User
    form_class = CandidateSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'candidate'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/admin/')