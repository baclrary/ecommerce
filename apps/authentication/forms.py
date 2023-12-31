from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from users.models import CustomUser, Profile


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2',
        'placeholder': 'e.g: john@gmail.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-200 border rounded text-xs font-medium leading-none text-gray-800 py-3 w-full pl-3 mt-2',
    }))

    error_messages = {
        'invalid_login': 'Invalid email or password',
    }


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'email',
            'type': 'email',
            'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2',
            'placeholder': 'e.g: john@gmail.com'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'myInput',
            'class': 'bg-gray-200 border rounded text-xs font-medium leading-none text-gray-800 py-3 w-full pl-3 mt-2',
        })
    )
    first_name = forms.CharField(
        required=True,
        label='First name',
        widget=forms.TextInput(attrs={
            'id': 'first_name',
            'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2',
            'placeholder': 'e.g: Tommy'
        })
    )
    middle_name = forms.CharField(
        required=False,
        label='Middle name',
        widget=forms.TextInput(attrs={
            'id': 'middle_name',
            'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2',
            'placeholder': 'e.g: Donald'
        })
    )
    last_name = forms.CharField(
        required=True,
        label='Last name',
        widget=forms.TextInput(attrs={
            'id': 'last_name',
            'class': 'bg-gray-200 border rounded text-xs font-medium leading-none placeholder-gray-800 text-gray-800 py-3 w-full pl-3 mt-2',
            'placeholder': 'e.g: Reuben'
        })
    )

    white_list_domains = ['gmail.com', 'yahoo.com', 'ukr.net']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(f"User with email {email} already exists.")
        domain = email.split('@')[-1]
        if domain not in self.white_list_domains:
            raise ValidationError(f"Sorry, but we do not support '{domain}' domain.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        for field_name in ['first_name', 'middle_name', 'last_name']:
            value = cleaned_data.get(field_name)
            if value:
                if len(value) > 20:
                    self.add_error(field_name,
                                   f"{self.fields[field_name].label} should not be longer than 20 characters.")
                elif len(value) < 3:
                    self.add_error(field_name, f"{self.fields[field_name].label} should be at least 3 characters.")

    def save(self):
        # Get cleaned data
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        first_name = self.cleaned_data.get('first_name')
        middle_name = self.cleaned_data.get('middle_name')
        last_name = self.cleaned_data.get('last_name')

        # Create user
        user = CustomUser.objects.create_user(email=email, password=password)

        # Create profile
        profile = Profile.objects.create(user=user, first_name=first_name,
                                         middle_name=middle_name, last_name=last_name)

        return user
