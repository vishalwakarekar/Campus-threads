# D:/miniproj/AluminiPortal/AlumniPortal/urls.py
from django.urls import path
from . import views

app_name = 'AlumniPortal'

urlpatterns = [
    # ... your other url patterns ...
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('events/', views.event_view, name='events'),
    path('assistant/', views.alumni_assistant_view, name='alumni_assistant'),

    # News URLs
    path('news/', views.news_list_view, name='news'), # For the list of all news
    path('news/<slug:slug>/', views.news_detail_view, name='news_detail'), # For a single news article

    # ... any other patterns ...
]


