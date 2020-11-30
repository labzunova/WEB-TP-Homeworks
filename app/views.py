from django.shortcuts import render, redirect
import random
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from app.models import Question, Answer
from app.models import Author
from app.forms import LoginForm, AskForm, SignupForm
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
    return render(request, 'ask.html', {})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                request.session['hello'] = 'world' # TODO
                auth.login(request, user)
                return redirect("/")  # TODO нужны правильные редиректы
            else:
                form.add_error(None, 'Wrong login or password')

    ctx = {'form': form}
    return render(request, 'login.html', ctx)


def signup(request):
    form = SignupForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('login')
        email = form.cleaned_data.get('email')
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        if password1 != password2:
            form.add_error(None, 'Passwords do not match!')
        elif User.objects.is_exist(username, email):
            form.add_error(None, 'This user already exist')
        else:
            user_ = User.objects.create_user(username, email, password1)
            User.objects.create(user=user_)
            auth.login(request, user_)
            return redirect('/')
    #varDict.update({'form': form})
    return render(request, 'signup.html', {'form': form})


def logout(request):
    auth.logout(request)
    # next_page = request.GET.get('stay', '/')
    # return redirect(next_page)
    return redirect("/login/")


def settings(request):
    return render(request, 'settings.html', {})


def default(request):
    return render(request, 'index.html', {})


def question_page(request, no):
    question = Question.objects.filter(identificator=no).first()
    answers = Answer.objects.filter(question=question)
    answers = paginate(request, answers)
    return render(request, 'question.html', {'question': question, 'answers': answers, 'page_obj': answers})
