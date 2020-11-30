from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
import random
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag
from app.models import Author
from app.forms import LoginForm, AskForm, SignupForm, SettingsForm, AnswerForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def paginate(request, object_list, per_page=5):
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    questions = Question.objects.new_questions()
    questions = paginate(request, questions)
    return render(request, 'index.html', {'questions': questions, 'page_obj': questions})


def index_hot(request):
    questions = Question.objects.best_questions()
    questions = paginate(request, questions)
    return render(request, 'index.html', {'questions': questions, 'page_obj': questions})


def index_by_tag(request, tag):
    questions_ = Question.objects.questions_by_tag(tag)
    questions = paginate(request, questions_)
    return render(request, 'index.html', {'questions': questions_, 'page_obj': questions})


@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        question = form.save(commit=False)
        question.author = request.user.author
        form.instance.user = Author.objects.get(user=request.user)
        question.identificator = Question.objects.all().count() + 1
        question.save()
        tags_ = form.cleaned_data.get("tags")
        question.tags.add(*tags_)
        question.save()
        return redirect(reverse('askcats_question', kwargs={'no': question.identificator}))
    ctx = {'form': form}
    return render(request, 'ask.html', ctx)


def login(request):
    page = request.GET.get('stay', '/')  # TODO
    if request.method == 'GET':
        form = LoginForm()
    else:
        redirect_to = request.GET.get('continue', '/')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                request.session['hello'] = 'world'  # TODO
                auth.login(request, user)
                return redirect(redirect_to)
            # return redirect("/")  # TODO нужны правильные редиректы
            else:
                form.add_error(None, 'Wrong login or password')
    redirect_to = request.GET.get('continue', '/')
    ctx = {'form': form, 'redirect_to': redirect_to}
    return render(request, 'login.html', ctx)


def signup(request):
    form = SignupForm(data=request.POST)
    if form.is_valid():
        username_ = form.cleaned_data.get('login')
        email = form.cleaned_data.get('email')
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        if password1 != password2:
            form.add_error(None, 'Passwords do not match!')
        elif User.objects.filter(username=username_).exists():
            form.add_error(None, 'This user already exist')
        else:
            user_ = User.objects.create_user(username_, email, password1)
            Author.objects.create(user=user_, user_name=username_)
            auth.login(request, user_)
            return redirect('/')
    return render(request, 'signup.html', {'form': form})


def logout(request):
    auth.logout(request)
    page = request.GET.get('stay', '/')
    return redirect(page)


# return redirect("/login/")


@login_required
def settings(request):
    init_data = {'login': request.user.username,
                 'email': request.user.email}
    author = Author.objects.filter(user=request.user)[0]
    form = SettingsForm(init_data, initial=init_data)
    if request.POST:
        form = SettingsForm(request.POST)
        if form.is_valid():
            name_field = form.cleaned_data.get('login')
            email_field = form.cleaned_data.get('email')
            password_field = form.cleaned_data.get('email')

            if name_field != request.user.username:
                if not Author.objects.new_name(author, name_field):
                    form.add_error(None, 'User with this name already exists')

            if email_field != request.user.email:
                if not Author.objects.new_email(author, email_field):
                    form.add_error(None, 'User with this email already exists')
    return render(request, 'settings.html', {'form': form})
    # return render(request, 'settings.html', {})


def default(request):
    return render(request, 'index.html', {})


def question_page(request, no):
    question_ = Question.objects.filter(identificator=no).first()
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.author
            answer.save()
            page = int(question_.answer_set.count() / 5) + 1
        return redirect(request.path + '?page=' + str(page) + '#' + str(answer.id))
    answers = Answer.objects.filter(question=question_)
    answers = paginate(request, answers)
    return render(request, 'question.html',
                  {'question': question_, 'answers': answers, 'page_obj': answers, 'form': form})
