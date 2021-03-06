from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag
from app.models import Author
from app.models import QuestionLikes, AnswerLikes
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
        question.identificator = Question.objects.all().count() + 1  # TODO
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
            request.session['hello'] = 'world'  # TODO
            auth.login(request, user)
            return redirect(redirect_to)

    redirect_to = request.GET.get('continue', '/')
    ctx = {'form': form, 'redirect_to': redirect_to}
    return render(request, 'login.html', ctx)


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
        if form.is_valid():
            username_ = form.cleaned_data.get('login')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
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
    if request.method == 'GET':
        form = SettingsForm(data={
            'login': request.user.username,
            'email': request.user.email
        })
    if request.POST:
        form = SettingsForm(data=request.POST, files=request.FILES,
                            instance=request.user.author)
        if form.is_valid():
            post = form.save(commit=False)
            username_field = form.cleaned_data.get('login')
            email_field = form.cleaned_data.get('email')
            author = request.user.author
            author.user_name = username_field
            author.avatar = request.FILES.get('avatar', request.user.author.avatar)
            author.save()

            user_ = request.user
            user_.username = username_field
            user_.email = email_field
            user_.save()

            form.save()
    return render(request, 'settings.html', {'form': form})


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
            form.instance.question = Question.objects.get(identificator=no)
            answer.save()
            question_.answers_count += 1
            question_.save(update_fields=['answers_count'])
            page = int(question_.answer_set.count() / 5) + 1
        return redirect(request.path + '?page=' + str(page) + '#' + str(answer.id))
    answers = Answer.objects.filter(question=question_)
    answers = paginate(request, answers)
    return render(request, 'question.html',
                  {'question': question_, 'answers': answers, 'page_obj': answers, 'form': form})


@require_POST
@login_required
def vote(request):
    data = request.POST
    if data['type'] == "question":
        entity = Question.objects.filter(identificator=data['id']).first()
        votion = QuestionLikes.objects.filter(question=entity, author=request.user.author).first()
        if votion is None:
            votion = QuestionLikes.objects.create(
                question=entity,
                author=request.user.author
            )
    else:
        entity = Answer.objects.filter(pk=data['id']).first()
        votion = AnswerLikes.objects.filter(answer=entity, author=request.user.author).first()
        if votion is None:
            votion = AnswerLikes.objects.create(
                answer=entity,
                author=request.user.author
            )

    if data['action'] == "like":
        if votion.vote == -1:  # отменить дизлайк + поставить лайк
            votion.vote = 1
            entity.rating = entity.rating + 2
        elif votion.vote == 0:  # просто поставить лайк, если его еще нет
            votion.vote = 1
            entity.rating = entity.rating + 1
        elif votion.vote == 1:  # отменить лайк
            votion.vote = 0
            entity.rating = entity.rating - 1
        else:
            return JsonResponse({"error": "smth went wrong"})
    elif data['action'] == "dislike":
        if votion.vote == -1:  # отменить дизлайк
            votion.vote = 0
            entity.rating = entity.rating + 1
        elif votion.vote == 0:  # просто поставить дизлайк, если его еще нет
            votion.vote = -1
            entity.rating = entity.rating - 1
        elif votion.vote == 1:  # отменить лайк и поставить дис
            votion.vote = -1
            entity.rating = entity.rating - 2
        else:
            return JsonResponse({"error": "smth went wrong"})
    votion.save()
    entity.save()
    response = {"rating": entity.rating}
    from pprint import pformat
    print(f'HERE: {pformat(response)}')
    return JsonResponse(response)


@require_POST
@login_required
def correct(request):
    data = request.POST
    answer = Answer.objects.filter(pk=data["aid"]).first()
    user = request.user.author
    old_right_ans = Answer.objects.filter(question__identificator=data["qid"], is_right=True).first()
    old_correct = ""
    if old_right_ans is None:
        answer.is_right = True
    else:
        old_right_ans.is_right = False
        old_correct = old_right_ans.pk
        answer.is_right = True
        old_right_ans.save()
    answer.save()
    return JsonResponse({"old_correct": old_correct})
