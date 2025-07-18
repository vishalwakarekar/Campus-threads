from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
# Added more validators
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.templatetags.static import static as staticfiles_url
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse # For get_absolute_url examples
import datetime # For batch_year validation

# --- Choices ---

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    ALUMNI = 'ALUMNI', 'Alumni'
    STUDENT = 'STUDENT', 'Student'

class Gender(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    OTHER = 'OTHER', 'Other'
    PREFER_NOT_TO_SAY = 'PNTS', 'Prefer not to say'

class ArticleStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PUBLISHED = 'PUBLISHED', 'Published'
    ARCHIVED = 'ARCHIVED', 'Archived'


# --- Validators ---

def validate_profile_photo_size(value):
    """Ensure profile photo size does not exceed 2MB."""
    limit_mb = 2
    limit_bytes = limit_mb * 1024 * 1024
    if value.size > limit_bytes:
        raise ValidationError(f'File too large. Size should not exceed {limit_mb} MB.')

# Optional: Phone number format validator
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

def current_year():
    """Get the current year."""
    return datetime.date.today().year

# --- Models ---

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, db_index=True)
    gr_number = models.CharField(max_length=11, null=True, blank=True, db_index=True, help_text="College GR Number e.g 22UGCS21242")
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, help_text="Optional phone number (e.g., +91XXXXXXXXXX).")
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)
    batch_year = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1950), MaxValueValidator(current_year() + 5)], db_index=True, help_text="Year of graduation (e.g., 2020).")
    department = models.CharField(max_length=100, blank=True, db_index=True, help_text="e.g., Computer Science, Mechanical")
    current_job_title = models.CharField(max_length=150, blank=True)
    company_name = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True, db_index=True, help_text="e.g., Pune, India")
    linkedin_profile = models.URLField(max_length=250, blank=True, help_text="Optional link to your LinkedIn profile.")
    achievements = models.TextField(blank=True, help_text="Highlight key achievements or contributions.")
    skills = models.TextField(blank=True, help_text="List professional or technical skills (comma-separated or one per line).")
    profile_photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True, validators=[validate_profile_photo_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], help_text="Upload a profile picture (Max 2MB, JPG/JPEG/PNG format).")
    bio = models.TextField(blank=True, help_text="A brief description about yourself, your journey, or interests.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username'] # Example ordering
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        try:
            identifier = self.user.get_username()
        except AttributeError:
            identifier = str(self.user.pk)
        return f"{identifier}'s Profile ({self.get_role_display()})"

    @property
    def full_name(self):
         name = self.user.get_full_name()
         try:
            identifier = self.user.get_username()
         except AttributeError:
             identifier = str(self.user.pk)
         return name if name else identifier

    def get_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        else:
            try:
                return staticfiles_url('AlumniPortal/images/default_avatar.png')
            except Exception:
                return None

# D:/miniproj/AluminiPortal/AlumniPortal/models.py
from django.db import models
from django.conf import settings # To get the User model
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class NewsArticle(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'), # Optional: for old articles you want to keep but not display prominently
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True,
                              help_text="A unique slug for the news article URL (will be auto-generated if left blank).")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Or models.CASCADE if an author's articles should be deleted with them
        null=True,
        blank=True,
        related_name='news_articles'
    )
    content = models.TextField(help_text="The main content of the news article.")
    summary = models.TextField(blank=True, null=True, help_text="A short summary or excerpt of the article (optional).")
    image = models.ImageField(
        upload_to='news_images/',
        blank=True,
        null=True,
        help_text="An optional image to accompany the news article."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="The current status of the news article (e.g., Draft, Published)."
    )
    published_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and time when the article was or will be published. If status is 'Published' and this is blank, it will be set to now."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: For tracking views, though this can also be done with a separate model or analytics
    # view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_date', '-created_at'] # Order by published_date first, then by creation
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug uniqueness if auto-generating
            original_slug = self.slug
            counter = 1
            while NewsArticle.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1

        # If an article is being published and doesn't have a published_date, set it to now.
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        # If an article is moved from published to draft, you might want to clear the published_date
        # elif self.status == 'draft' and self.published_date:
        #     self.published_date = None # Optional: depends on desired behavior

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Returns the canonical URL for a news article.
        Assumes you have a URL pattern named 'news_detail' that takes a 'slug'.
        """
        if self.status == 'published' and self.slug:
            return reverse('AlumniPortal:news_detail', kwargs={'slug': self.slug})
        return None # Or a fallback URL, or raise an exception

    @property
    def is_published(self):
        """
        A convenience property to check if the article is considered published.
        This can be useful if your definition of "published" becomes more complex.
        """
        return self.status == 'published' and (self.published_date is not None and self.published_date <= timezone.now())


# --- Event Model Added Back ---
class EventType(models.TextChoices):
    NETWORKING = 'NETWORKING', 'Networking'
    WORKSHOP = 'WORKSHOP', 'Workshop'
    SEMINAR = 'SEMINAR', 'Seminar'
    REUNION = 'REUNION', 'Reunion'
    WEBINAR = 'WEBINAR', 'Webinar'
    OTHER = 'OTHER', 'Other'

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True, db_index=True)
    description = models.TextField()
    event_type = models.CharField(max_length=100, choices=EventType.choices, default=EventType.OTHER, db_index=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organized_events'
    )
    # Only ONE definition for attendees
    # attendees = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='attended_events', # Ensure this related_name is unique if you have other M2M to User
    #     blank=True
    # )
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time', 'title']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            queryset = Event.objects.all()
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            while queryset.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('AlumniPortal:event_detail', kwargs={'slug': self.slug})
        except Exception:
            return "#"