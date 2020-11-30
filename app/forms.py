from django import forms
from app.models import Question, Author
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.Form):
    login = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

