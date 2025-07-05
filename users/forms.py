from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class UserAuthenticationForm(AuthenticationForm):
    pass


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=255)


class PasswordResetForm(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')


class BlockingUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']