from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=500)
    zipcode = models.PositiveIntegerField()
    skills = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
