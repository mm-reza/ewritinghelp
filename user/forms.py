from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput
from.models import UserProfile



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name :')
    email = forms.EmailField(required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Email is already registered")
        return self.cleaned_data['email']

    first_name = forms.CharField(
        max_length=50, label='First Name :')
    last_name = forms.CharField(
        max_length=50, label='Last Name :')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2', )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'country', 'city', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'city'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
        }
