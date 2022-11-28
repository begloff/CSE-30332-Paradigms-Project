from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Candidate, Recruiter, User
from django.db import transaction
from django.forms.utils import ValidationError

class CandidateSignUpForm(UserCreationForm):
    name = forms.CharField(
        required=True,
        max_length=200
    )
    bio = forms.CharField(
        max_length=500,
        required=False,
    )
    zip = forms.IntegerField(
        required=True
    )
    skills = forms.CharField(
        required=True,
        max_length=200        
    )
    github = forms.CharField(
        max_length=100,
        required=False,        
    )
    experience = forms.IntegerField(
        required=True       
    )
    education = forms.CharField(
        max_length=100,
        required=False,        
    )

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_candidate = True
        user.save()
    

        candidate = Candidate.objects.create(user=user)
        candidate.name = self.cleaned_data.get('name')
        candidate.bio = self.cleaned_data.get('bio')
        candidate.zip = self.cleaned_data.get('zip')
        candidate.skills = self.cleaned_data.get('skills')
        candidate.github = self.cleaned_data.get('github')
        candidate.experience = self.cleaned_data.get('experience')
        candidate.education = self.cleaned_data.get('education')
        candidate.save()

        return user


class RecruiterSignUpForm(UserCreationForm):
    name = forms.CharField(
        required=True,
        max_length=200
    )
    company = forms.CharField(
        max_length=500,
        required=True,
    )
    zip = forms.IntegerField(
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_recruiter = True
        user.save()
    

        recruiter = Recruiter.objects.create(user=user)
        recruiter.name = self.cleaned_data.get('name')
        recruiter.bio = self.cleaned_data.get('company')
        recruiter.zip = self.cleaned_data.get('zip')

        recruiter.save()

        return user


    