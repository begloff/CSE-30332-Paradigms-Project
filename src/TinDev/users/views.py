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

    #Candidate SignUp View returns form for creating new candidate

    model = User
    form_class = CandidateSignUpForm #Uses form from forms.py
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'candidate'
        return super().get_context_data(**kwargs)

    def form_valid(self, form): #Method that runs on form submit
        user = form.save()
        login(self.request, user)
        return redirect('/') #Go to home page logged in

class RecruiterSignUpView(CreateView):
    #SignUp views for recruiter

    model = User
    form_class = RecruiterSignUpForm #Uses form from forms.py
    template_name = 'registration/signup_form.html' #Template to reference

    def get_context_data(self, **kwargs): #Specifies user type as recruiter
        kwargs['user_type'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form): #Method that runs on form submit
        user = form.save()
        login(self.request, user)
        return redirect('/')

class CreatePostView(CreateView):

    #Creates new post using the given fields for the form

    model = Post
    fields = ('position_title', 'description', 'job_type', 'job_city', 'job_state', 'skills', 'company', 'expiration_date')
    template_name = 'recruiter/create_post.html'

    def form_valid(self, form): #Runs on form submit
        post = form.save(commit = False)
        post.user = self.request.user
        post.save()
        return redirect('/recruiter/post/view/all')


class PostIndexViewAll(ListView):

    #Lists all of posts for candidate

    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.annotate(num_interested=Count('interests')).filter(user=self.request.user).order_by('-is_active','-expiration_date') #Orders by active posts, then decending expr date

class PostIndexViewActive(ListView):

    #Same as PostIndexViewAll but just active posts

    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.annotate(num_interested=Count('interests')).filter(user=self.request.user, is_active=True).order_by('-is_active','-expiration_date')

class PostIndexViewInactive(ListView):

    # Same as PostIndexViewAll just inactive posts though

    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.annotate(num_interested=Count('interests')).filter(user=self.request.user, is_active=False).order_by('-is_active','-expiration_date')

class PostUpdateView(UpdateView):

    #View for updating post details

    model = Post
    template_name = "recruiter/post-update.html"
    fields = ('position_title', 'description', 'job_type', 'job_city', 'job_state', 'skills', 'company', 'expiration_date', 'is_active') #Specifies form fields
    
    success_url = "/recruiter/post/view/all" #On success redirect to here

class PostDeleteView(DeleteView):

    #Deletes given post (Deletion handled by DeleteView)

    model = Post
    template_name = "recruiter/post_confirm_delete.html"
    success_url = "/recruiter/post/view/all"
    context_object_name = 'post'

class CandidatePostIndexViewAll(ListView):

    #Filters candidate posts based on all Indexes

    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs): #Ran whenever getting data for list view
        return Post.objects.order_by('-is_active','-expiration_date')

class CandidatePostIndexViewActive(ListView):

    #Same as CandidatePostIndexViewAll but with only inactive listings

    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(is_active=True).order_by('-is_active','-expiration_date')

class CandidatePostIndexViewInactive(ListView):

    #Same as CandidatePostIndexViewAll but only inactive listings

    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(is_active=False).order_by('-is_active','-expiration_date')

class CandidatePostIndexViewIntrested(ListView):

    #Same as CandidatePostIndexViewAll but for posts that user is interested in

    model = Post
    template_name = 'candidate/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(interests__user=self.request.user).order_by('-is_active','-expiration_date')


class LocationSearchResults(ListView):

    #Search jobs based on city and state fields

    model = Post
    template_name = "candidate/search_results.html"
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q") #Get from url the specified query
        return Post.objects.filter(Q(job_city__icontains=query) | Q(job_state__icontains=query)) #Return objects that contain queried location

class KeywordSearchResults(ListView):

    #Similar to LocationSearchResults

    model = Post
    template_name = "candidate/search_results.html"
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs): 
        query = self.request.GET.get("q")
        return Post.objects.filter(Q(description__icontains=query)) #Searches job desc for said query

class PostIndexViewInterest(ListView):

    #Checks number of interested users for each post and filters, accepting only greater than 0

    model = Post
    template_name = 'recruiter/view_posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.annotate(num_interested=Count('interests')).filter(user=self.request.user, num_interested__gt=0).order_by('-is_active','-expiration_date')

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
    Offer.objects.filter(duedate__lt=datetime.date.today()).update(is_active=False)
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

def acceptOffer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.accepted = True
    offer.save()
    return redirect("/candidate/offer/view")

def declineOffer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.declined = True
    offer.save()
    return redirect("/candidate/offer/view")