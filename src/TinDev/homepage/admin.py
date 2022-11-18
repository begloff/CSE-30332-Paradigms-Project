from django.contrib import admin

from .models import Candidate, Recruiter

admin.site.register(Candidate)
admin.site.register(Recruiter)
