from django import forms
from app.models import Question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

