from PIL import Image
from django import forms
from app.models import Question, Author, Answer
from django.contrib.auth.models import User
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        # если пользователь не зарегистрирован, возвращаем сообщение об ошибке
        if user is None:
            raise forms.ValidationError("Invalid login or password. Please try again.")
        return self.cleaned_data


class SignupForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def clean_login(self):
        cleaned_data = super(SignupForm, self).clean()
        if User.objects.filter(username=cleaned_data['login']).exists():
            raise forms.ValidationError('User with this login already exists')
        return cleaned_data['login']


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    error_messages = {'title': {'required': 'Enter a title'},
                      'text': {'required': 'Enter a question text'}}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = {
            "text": "Your answer",
        }


class SettingsForm(forms.ModelForm):
    login = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Author
        fields = ["avatar"]

    # def clean(self):
    #     cleaned_data = super(SettingsForm, self).clean()
    #     if User.objects.filter(username=cleaned_data['login']).exists():
    #         raise forms.ValidationError('User with this login already exists')
    #     if User.objects.filter(email=cleaned_data['email']).exists():
    #         raise forms.ValidationError('User with this email already exists')
    #     return cleaned_data
