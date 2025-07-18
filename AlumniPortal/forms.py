# D:/minip/AlumniTKIET/AlumniPortal/forms.py

from django import forms
# from django.contrib.auth.forms import UserCreationForm # Import if creating a custom registration form
# from django.contrib.auth.models import User # Import User if modifying user fields directly
from .models import Profile, Gender # Import models and choices needed for forms

# --- Profile Editing Form ---
class ProfileForm(forms.ModelForm):
    """
    Form for users to edit their own profile details.
    """
    # Optional: If you want to edit User fields (like first/last name) alongside Profile fields
    # first_name = forms.CharField(max_length=150, required=False, label="First Name")
    # last_name = forms.CharField(max_length=150, required=False, label="Last Name")
    # email = forms.EmailField(required=False, label="Email Address") # Be cautious allowing email changes

    class Meta:
        model = Profile
        # Include fields users should be able to edit from their profile page
        # Exclude 'user' (set automatically) and 'role' (usually managed by admin)
        fields = [
            # 'first_name', 'last_name', 'email', # Add if editing User fields too
            'phone_number', 'gender', 'batch_year', 'department',
            'current_job_title', 'company_name', 'industry', 'location',
            'linkedin_profile', 'achievements', 'skills', 'profile_photo', 'bio'
        ]

        # Use widgets to customize the appearance and behavior of form fields
        widgets = {
            'gender': forms.Select(), # Automatically uses choices from the model field
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us a bit about yourself...'}),
            'achievements': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List key achievements...'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Python, Project Management, Public Speaking'}),
            # Use specific input types for better browser handling and validation
            'batch_year': forms.NumberInput(attrs={'min': 1950, 'max': 2099, 'placeholder': 'YYYY'}), # Example range
            'linkedin_profile': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'profile_photo': forms.ClearableFileInput(attrs={'accept': 'image/png, image/jpeg'}) # Hint for file types
        }

        # Optional: Add labels or help texts if different from model definitions
        labels = {
            'current_job_title': 'Current Position/Job Title',
            'batch_year': 'Batch (Year of Graduation)',
            'profile_photo': 'Profile Picture',
        }
        help_texts = {
            'phone_number': 'Enter with country code if applicable.',
            'skills': 'Separate skills with commas or new lines.',
        }

    # Optional: If editing User fields, you might need to override __init__ and save
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Populate User fields if editing them
    #     if self.instance and self.instance.user:
    #         self.fields['first_name'].initial = self.instance.user.first_name
    #         self.fields['last_name'].initial = self.instance.user.last_name
    #         self.fields['email'].initial = self.instance.user.email

    # def save(self, commit=True):
    #     profile = super().save(commit=False) # Get the profile instance but don't save yet
    #     # Save User fields if editing them
    #     if self.instance and self.instance.user:
    #         user = self.instance.user
    #         user.first_name = self.cleaned_data.get('first_name', user.first_name)
    #         user.last_name = self.cleaned_data.get('last_name', user.last_name)
    #         user.email = self.cleaned_data.get('email', user.email) # Handle email changes carefully
    #         if commit:
    #             user.save()
    #
    #     if commit:
    #         profile.save() # Save the profile instance
    #         self.save_m2m() # Needed if you have ManyToManyFields
    #     return profile

# --- Custom Registration Form (Optional Example) ---
# Only needed if Django's default UserCreationForm isn't sufficient.
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class UserRegistrationForm(UserCreationForm):
#     # Add extra fields here if needed during registration
#     first_name = forms.CharField(max_length=150, required=True)
#     last_name = forms.CharField(max_length=150, required=True)
#     email = forms.EmailField(required=True) # Making email required explicitly

#     class Meta(UserCreationForm.Meta):
#         model = User
#         # Add fields from User model you want on the registration form
#         fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

#     # You might override save() here if you need to create the Profile
#     # immediately and potentially set fields based on registration form data.
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         # Set additional fields before saving
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#             # Create profile after user is saved
#             if Profile: # Check if Profile model exists
#                 Profile.objects.create(user=user) # Creates profile with default role
#         return user