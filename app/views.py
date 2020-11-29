from django.shortcuts import render, get_object_or_404, redirect, reverse
import random
from django.core.paginator import Paginator
from app.models import Question
from app.models import Answer
from app.forms import LoginForm, AskForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def paginate(request, object_list, per_page=5):
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    print(f'HELLO: {request.session.get("hello")}')
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


def settings(request):
    return render(request, 'settings.html', {})


def default(request):
    return render(request, 'index.html', {})


def question_page(request, no):
    question = Question.objects.filter(identificator=no).first()
    answers = Answer.objects.filter(question=question)
    answers = paginate(request, answers)
    return render(request, 'question.html', {'question': question, 'answers': answers, 'page_obj': answers})


@login_required  # TODO not working
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question = request.author = request.user.author
            question.save()
            return redirect(reverse('question', kwargs={'qid': question.pk}))
    ctx = {'form': form}
    return render(request, 'ask.html', ctx)


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
    ctx = {'form': form}
    return render(request, 'login.html', ctx)


def signup(request):
    return render(request, 'signup.html', {})


def logout(request):
    auth.logout(request)
    return redirect("/")
