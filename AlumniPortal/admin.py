# # D:/miniproj/AluminiPortal/AlumniPortal/admin.py
#
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth import get_user_model
# # Import all relevant models from your app (re-added Event, EventType)
# from .models import Profile, NewsArticle, Event, EventType
# from django.utils.html import format_html
# from django.utils.translation import gettext_lazy as _ # For better admin display names
#
# User = get_user_model()
#
# # --- Inline Admin for Profile (Displayed within User Admin) ---
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'
#     # Limit fields shown inline for clarity, or show more if needed
#     fields = ('role', 'gr_number', 'batch_year', 'department', 'profile_photo')
#     extra = 0 # Don't show extra empty forms
#     raw_id_fields = ('user',) # Use search popup for user selection
#
# # --- Custom User Admin ---
# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role', 'get_gr_number')
#     list_select_related = ('profile',) # Optimize query to fetch profile data
#
#     @admin.display(description=_('Role')) # Use translated description
#     def get_role(self, instance):
#         profile = getattr(instance, 'profile', None)
#         if profile:
#             return profile.get_role_display()
#         return _('N/A') # Use translated 'N/A'
#
#     @admin.display(description=_('GR Number'), ordering='profile__gr_number')
#     def get_gr_number(self, instance):
#         profile = getattr(instance, 'profile', None)
#         if profile and profile.gr_number:
#             return profile.gr_number
#         return _('N/A')
#
#     # Allow searching users by their profile's GR number
#     search_fields = BaseUserAdmin.search_fields + ('profile__gr_number',)
#
# # --- Profile Admin ---
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'gr_number', 'full_name', 'role', 'batch_year', 'department', 'updated_at')
#     list_filter = ('role', 'batch_year', 'department', 'updated_at')
#     search_fields = ('gr_number', 'user__username', 'user__first_name', 'user__last_name', 'department', 'company_name')
#     ordering = ('user__username',)
#     readonly_fields = ('created_at', 'updated_at',)
#     fieldsets = (
#         (None, {'fields': ('user', 'role')}),
#         (_('Basic Information'), {'fields': ('gr_number', 'phone_number', 'gender', 'batch_year', 'department')}),
#         (_('Professional Details'), {'fields': ('current_job_title', 'company_name', 'industry', 'location', 'linkedin_profile')}),
#         (_('Profile Content'), {'fields': ('profile_photo', 'bio', 'achievements', 'skills')}),
#         (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
#     )
#     raw_id_fields = ('user',) # Use search popup for user selection
#
# # --- News Article Admin ---
# @admin.register(NewsArticle)
# class NewsArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'status', 'published_date', 'created_at')
#     list_filter = ('status', 'author', 'published_date', 'created_at')
#     search_fields = ('title', 'content', 'author__username', 'author__email')
#     ordering = ('-status', '-published_date', '-created_at')
#     # Slug is auto-generated, make it read-only
#     readonly_fields = ('created_at', 'updated_at', 'slug')
#     # Auto-populate slug from title in the admin form
#     prepopulated_fields = {'slug': ('title',)}
#
#     fieldsets = (
#         (None, {'fields': ('title', 'slug', 'status')}),
#         (_('Content'), {'fields': ('content', 'image')}),
#         (_('Publication'), {'fields': ('author', 'published_date')}),
#         (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
#     )
#     raw_id_fields = ('author',) # Use search popup for author selection
#
#     # Automatically set author to current user on creation if not set
#     def save_model(self, request, obj, form, change):
#         if not obj.author_id:
#             obj.author = request.user
#         super().save_model(request, obj, form, change)
#
# # --- Event Admin (Added Back) ---
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'event_type', 'start_time', 'end_time', 'location', 'organizer', 'created_at')
#     list_filter = ('event_type', 'start_time', 'location', 'organizer')
#     search_fields = ('title', 'description', 'location', 'organizer__username', 'organizer__email')
#     ordering = ('-start_time',)
#     readonly_fields = ('created_at', 'updated_at', 'slug')
#     prepopulated_fields = {'slug': ('title',)}
#     # Use raw_id_fields for ForeignKey and ManyToManyField if user list is large
#     raw_id_fields = ('organizer', 'attendees')
#     # Use filter_horizontal for a better ManyToMany interface if preferred
#     # filter_horizontal = ('attendees',)
#
#     fieldsets = (
#         (None, {'fields': ('title', 'slug', 'event_type')}),
#         (_('Details'), {'fields': ('description', 'location')}),
#         (_('Timing'), {'fields': ('start_time', 'end_time')}),
#         (_('Participants'), {'fields': ('organizer', 'attendees')}),
#         # Optional: Add image field if you uncomment it in models.py
#         # (_('Visuals'), {'fields': ('image',)}),
#         (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
#     )
#
# # --- Registering User Admin ---
# # Unregister the default User admin first to avoid conflicts
# try:
#     admin.site.unregister(User)
# except admin.sites.NotRegistered:
#     pass # Ignore if User wasn't registered before
#
# # Register the User model with our custom UserAdmin
# admin.site.register(User, UserAdmin)
#
# # Note: EventType doesn't usually need its own admin registration unless you
# # want to manage the choices directly via the admin (which is uncommon for TextChoices).


from django.contrib import admin
from .models import Profile,Event,NewsArticle,EventType
from django.utils.translation import gettext_lazy as _

admin.site.register(Profile)
# admin.site.register(Event)
admin.site.register(NewsArticle)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Event model.
    """
    list_display = (
        'title',
        'event_type',
        'start_time',
        'location',
        'is_published',
        'organizer_display' # Custom display for organizer
    )
    list_filter = ('is_published', 'event_type', 'start_time')
    search_fields = ('title', 'description', 'location', 'organizer__username', 'organizer__email')
    ordering = ('-start_time',) # Show upcoming or most recent first

    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug from title

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'is_published', 'event_type')
        }),
        (_('Content & Media'), {
            'fields': ('description', 'image')
        }),
        (_('Date, Time & Location'), {
            'fields': ('start_time', 'end_time', 'location')
        }),
        (_('Organization & Participation'), {
            'fields': ('organizer', )
        }),
        (_('Timestamps (Read-only)'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Make this section collapsible
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('organizer',) # Better UI for selecting organizer if many users
    # filter_horizontal = ('attendees',) # Better UI for ManyToManyField 'attendees'

    actions = ['publish_events', 'unpublish_events']

    @admin.display(description=_('Organizer'), ordering='organizer__username')
    def organizer_display(self, obj):
        if obj.organizer:
            return obj.organizer.get_full_name() or obj.organizer.username
        return _("N/A")

    def publish_events(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, _("Selected events have been published."))
    publish_events.short_description = _("Publish selected events")

    def unpublish_events(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, _("Selected events have been unpublished."))
    unpublish_events.short_description = _("Unpublish selected events")



# admin.site.register(EventType)
# AlumniPortal/admin.py

