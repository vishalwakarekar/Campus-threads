# D:/miniproj/AluminiPortal/AlumniPortal/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Profile, Role
from django.contrib.auth import get_user_model
from .models import NewsArticle,Event
from django.utils import timezone
from django.core.exceptions import FieldError
from django.db.models import Q # Already imported, good for event search

User = get_user_model()

# --- Forms ---
# (Your CustomUserCreationForm and ProfileForm are here)
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email address is required.")
        if User.objects.filter(email=email).exists():
             raise forms.ValidationError("A user with this email address already exists.")
        return email

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = [
            'phone_number', 'gender', 'batch_year', 'department',
            'current_job_title', 'company_name', 'industry', 'location',
            'linkedin_profile', 'achievements', 'skills', 'profile_photo', 'bio'
        ]
        exclude = ['user', 'role']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'achievements': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'batch_year': forms.NumberInput(attrs={'min': 1950, 'max': 2099}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            if self.instance.profile_photo:
                 self.fields['profile_photo'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("Another user is already registered with this email address.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

# --- Views ---

# def home(request):
#     context = {'page_title': 'Welcome to the Alumni Portal'}
#     return render(request, 'AlumniPortal/home.html', context)


# D:/miniproj/AluminiPortal/AlumniPortal/views.py
from django.shortcuts import render
from .models import NewsArticle, Event # Make sure to import your models
# from django.utils import timezone # Keep this if you use it for upcoming events


def home_view(request): # Or whatever your home view is named
    # Fetch the latest 3 news articles
    # Assuming 'published' is the value in your 'status' field for published articles
    # Adjust 'published' if your status value is different (e.g., 'P', 1, etc.)
    latest_news = NewsArticle.objects.filter(status='published').order_by('-published_date')[:3]

    # Fetch the latest 3 events.
    # Using the 'is_published' field for events as indicated by the error message choices.
    latest_events = Event.objects.filter(is_published=True).order_by('-created_at')[:3]

    # Alternative for upcoming events (if you prefer that for the home page)
    # from django.utils import timezone
    # upcoming_events = Event.objects.filter(is_published=True, start_time__gte=timezone.now()).order_by('start_time')[:3]
    # latest_events = upcoming_events # if you choose this option

    context = {
        'page_title': "Welcome - TKIET Alumni Portal",
        'latest_news_articles': latest_news,
        'latest_events_list': latest_events,
    }
    return render(request, 'AlumniPortal/home.html', context)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=Role.STUDENT)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('AlumniPortal:view_profile')
        else:
             messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def log_out(request):
    logout(request)
    return redirect('login') # Make sure you have a URL named 'login'

@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {
        'profile': profile,
        'page_title': f"{profile.full_name}'s Profile"
    }
    return render(request, 'AlumniPortal/profile_view.html', context)

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('AlumniPortal:view_profile')
        else:
             messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form,
        'profile': profile,
        'page_title': 'Edit Your Profile'
    }
    return render(request, 'AlumniPortal/profile_form.html', context)

def about_view(request):
    context = {'page_title': 'About Us'}
    return render(request, 'AlumniPortal/about.html', context)

def contact_view(request):
    context = {'page_title': 'Contact Us'}
    return render(request, 'AlumniPortal/contact.html', context)

def event_view(request):
    now = timezone.now()
    event_list_qs = Event.objects.filter(is_published=True).order_by('start_time')
    query = request.GET.get('q')
    if query:
        event_list_qs = event_list_qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(event_type__icontains=query)
        ).distinct()

    paginator = Paginator(event_list_qs, 10)
    page_number = request.GET.get('page')
    try:
        events_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        events_page_obj = paginator.page(1)
    except EmptyPage:
        events_page_obj = paginator.page(paginator.num_pages)

    context = {
        'events': events_page_obj,
        'is_paginated': events_page_obj.has_other_pages(),
        'page_obj': events_page_obj,
        'page_title': 'Upcoming Events',
        'query': query,
    }
    return render(request, 'AlumniPortal/events.html', context)

# --- News Views ---

def news_list_view(request): # Renamed from news_detail_view and removed slug
    """
    Displays a list of published news articles with pagination.
    """
    now = timezone.now()
    all_articles_qs = NewsArticle.objects.filter(
        status='published',
        published_date__lte=now
    ).order_by('-published_date')

    # --- DEBUGGING (can be removed once confirmed working) ---
    # print(f"Found {all_articles_qs.count()} articles matching criteria.")
    # for article_debug in all_articles_qs:
    #     print(f"  - Title: {article_debug.title}, Status: {article_debug.status}, Published Date: {article_debug.published_date}")
    # --- END DEBUGGING ---

    paginator = Paginator(all_articles_qs, 9) # Show 9 news articles per page
    page_number = request.GET.get('page')

    try:
        news_articles_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        news_articles_page_obj = paginator.page(1)
    except EmptyPage:
        news_articles_page_obj = paginator.page(paginator.num_pages)

    context = {
        'news_articles': news_articles_page_obj, # This is the page object
        'is_paginated': news_articles_page_obj.has_other_pages(),
        'page_obj': news_articles_page_obj, # Pass the page object itself for pagination template
        'page_title': 'Latest News',
    }
    # Ensure this template exists: templates/AlumniPortal/news.html
    return render(request, 'AlumniPortal/news.html', context)


def news_detail_view(request, slug): # This was previously news_list_view(request, slug)
    """
    Displays a single news article.
    """
    now = timezone.now()
    article = get_object_or_404(
        NewsArticle,
        slug=slug,
        status='published',
        published_date__lte=now
    )
    context = {
        'article': article,
        'page_title': article.title,
    }
    # Ensure this template exists: templates/AlumniPortal/news_detail.html
    return render(request, 'AlumniPortal/news_detail.html', context)



def alumni_assistant_view(request):
    """
    Renders the Alumni Assistant chatbot page.
    """
    return render(request, 'AlumniPortal/riruru.html')