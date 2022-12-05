from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

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
    name = models.CharField(max_length=200,default='')
    company = models.CharField(max_length=50,default='')
    zipcode = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Include User? May Mess with creating and editing
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=100,default='')
    job_type = models.CharField(max_length=100,default='')
    job_city = models.CharField(max_length=100,default='')
    job_state = models.CharField(max_length=100,default='')
    skills = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=500,default='')
    company = models.CharField(max_length=100,default='')
    expiration_date = models.DateField(default=datetime.date.today)
    is_active = models.BooleanField(default = False)

    def __str__(self):
        return f'Post for {self.position_title} made by {self.user.username}'