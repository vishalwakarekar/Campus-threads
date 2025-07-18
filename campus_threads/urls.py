# campus_threads/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings              # Import settings
from django.conf.urls.static import static  # Import static

from AlumniPortal import views

urlpatterns = [
    path('accounts/login/admin/', admin.site.urls,name='admin'),
    path('', include('AlumniPortal.urls')), # Your app's URLs
    path('accounts/', include('django.contrib.auth.urls')),

path('', views.home_view, name='home'),

path('register', views.register_view, name='register'),
    path('logout', views.log_out, name='logout'),

    # Auth URLs
path('events',views.event_view,name='events'),

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('news/', views.news_list_view, name='news'),  # Use news_list_view and add a trailing slash


]

# Add this line ONLY if DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Serves static files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)     # Serves media files (like profile photos)
