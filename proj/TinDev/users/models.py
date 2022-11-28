from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_candidate = models.BooleanField(default = False)
    is_recruiter = models.BooleanField(default = False)

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    bio = models.CharField(max_length=500, default='')
    zipcode = models.PositiveIntegerField(default=0)
    skills = models.CharField(max_length=200, default='')
    experience = models.IntegerField(default=0)
    github = models.CharField(max_length=100, default='')
    education = models.CharField(max_length=100, default='')


    def __str__(self):
        return self.user.username

class Recruiter(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=50)
    zipcode = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
