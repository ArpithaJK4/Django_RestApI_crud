from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# ✅ Form for User Registration
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password",
        help_text=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password",
        help_text=''
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth",
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'name', 'phone_no', 'location', 'dob']


# ✅ Form for Updating User Profile
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_no', 'location', 'dob']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
