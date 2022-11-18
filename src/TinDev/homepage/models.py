from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=500)
    zipcode = models.PositiveIntegerField()
    skills = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Recruiter(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=50)
    zipcode = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
