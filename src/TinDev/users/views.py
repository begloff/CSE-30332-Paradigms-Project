from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import User, Post, Candidate, Offer
from .forms import CandidateSignUpForm, RecruiterSignUpForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse


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
        return redirect('/')

class RecruiterSignUpView(CreateView):
    model = User
    form_class = RecruiterSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class CreatePostView(CreateView):
    model = Post
    fields = ('position_title', 'description', 'job_type', 'job_city', 'job_state', 'skills', 'company', 'expiration_date')
    template_name = 'recruiter/create_post.html'

    def form_valid(self, form):
        post = form.save(commit = False)
        post.user = self.request.user
        post.save()
        messages.success(self.request, 'The post was created successfully.')
        return redirect('/recruiter/post/view/all')


class PostIndexViewAll(ListView):
    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(user=self.request.user).order_by('-is_active','-expiration_date')

class PostIndexViewActive(ListView):
    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(user=self.request.user, is_active=True).order_by('-is_active','-expiration_date')

class PostIndexViewInactive(ListView):
    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(user=self.request.user, is_active=False).order_by('-is_active','-expiration_date')

class PostUpdateView(UpdateView):
    model = Post
    template_name = "recruiter/post-update.html"
    fields = ('position_title', 'description', 'job_type', 'job_city', 'job_state', 'skills', 'company', 'expiration_date', 'is_active')
    
    success_url = "/recruiter/post/view/all"

class PostDeleteView(DeleteView):
    model = Post
    template_name = "recruiter/post_confirm_delete.html"
    success_url = "recruiter/post/view/all"
    context_object_name = 'post'

class CandidatePostIndexViewAll(ListView):
    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.order_by('-is_active','-expiration_date')

class CandidatePostIndexViewActive(ListView):
    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(is_active=True).order_by('-is_active','-expiration_date')

class CandidatePostIndexViewInactive(ListView):
    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(is_active=False).order_by('-is_active','-expiration_date')

class LocationSearchResults(ListView):
    model = Post
    template_name = "candidate/search_results.html"
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        return Post.objects.filter(Q(job_city__icontains=query) | Q(job_state__icontains=query))

class KeywordSearchResults(ListView):
    model = Post
    template_name = "candidate/search_results.html"
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        return Post.objects.filter(Q(description__icontains=query))

class PostIndexViewInterest(ListView):
    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.annotate(num_candidates=Count('interests')).filter(user=self.request.user, num_candidates__gt=0).order_by('-is_active','-expiration_date')

def PostDetailView(request, pk):

    post = get_object_or_404(Post, pk=pk)
    matching = {}

    #Loop through interested candidates in post and get object
    for candidate in post.interests.all():
        total = 0
        #Scan skills in candidates and job desc and match based on that
        for s1 in candidate.skills.split(", "):
            for s2 in post.skills.split(", "):
                if( s1 == s2 ):
                    total += 1

        #Make dictionary storing that
        x = (total / 5) * 100
        if total > 5:
            x = 100
        matching[candidate] = x
    #Rough Scale: 5 matched skills = 100%



    context = {}
    context['post'] = post
    context['matching'] = matching

    return render(request, 'recruiter/post_details.html', context)



class CreateOffer(CreateView):
    model = Offer
    fields = ('salary', 'duedate')
    template_name = 'recruiter/create_offer.html'

    def form_valid(self, form):
        offer = form.save(commit = False)
        offer.candidate = get_object_or_404(Candidate, pk=self.request.GET.get('user_id'))
        offer.post = get_object_or_404(Post, pk=self.request.GET.get('post_id'))
        offer.save()
        messages.success(self.request, 'The offer was created successfully.')
        return redirect('/recruiter/post/view/all')

class ViewOffers(ListView):
    model = Offer
    template_name = 'candidate/view_offers.html'
    context_object_name = 'offer_list'

    def get_queryset(self, *args, **kwargs):
        return Offer.objects.filter(candidate__user=self.request.user).order_by('-duedate') 


import datetime

def home(request):
    Post.objects.filter(expiration_date__lt=datetime.date.today()).update(is_active=False)
    return render(request, 'home.html')

def addInterest(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    candidate = get_object_or_404(Candidate, pk=request.user)
    post.interests.add(candidate)
    post.save()
    return redirect("/candidate/post/view/all")

def removeInterest(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    candidate = get_object_or_404(Candidate, pk=request.user)
    post.interests.remove(candidate)
    post.save()
    return redirect("/candidate/post/view/all")