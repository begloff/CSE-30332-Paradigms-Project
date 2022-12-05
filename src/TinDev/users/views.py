from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import User, Post, Candidate
from .forms import CandidateSignUpForm, RecruiterSignUpForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
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
    fields = ('position_title', 'description', 'job_type', 'job_city', 'job_state', 'skills', 'company', 'expiration_date', 'is_active')
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


def home(request):
    return render(request, 'home.html')

def addInterest(request, post_id):

    #Can hopefully just Use user rather than candidate
    post = get_object_or_404(Post,pk=post_id)

    if request.user.is_authenticated:
        user_id = request.user.id

    post.candidates.add(user_id)

    post.save()

    return render(request, 'home.html')

