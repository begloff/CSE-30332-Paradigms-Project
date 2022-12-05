from django.contrib import admin
from .models import User, Candidate, Recruiter, Post



# Register your models here.
admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Post)