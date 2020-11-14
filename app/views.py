from django.shortcuts import render
import random
from django.core.paginator import Paginator
from app.models import Question
from app.models import Answer

def paginate(request, object_list, per_page=5):
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

answers = [
    {
    	'id': idx,
    	'text':'answer'
    } for idx in range(5)
]

def index(request):
    questions = Question.objects.new_questions()
    page_obj = paginate(request, questions)
    return render(request,'index.html', {'questions':questions, 'page_obj': page_obj})
    
def index_hot(request):
    questions = Question.objects.best_questions()
    page_obj = paginate(request, questions)
    return render(request,'index.html', {'questions':questions, 'page_obj': page_obj})
       
def index_by_tag(request, tag):
    questions = Question.objects.tag_questions(tag)
    page_obj = paginate(request, questions)
    return render(request,'index.html', {'questions':questions, 'page_obj': page_obj}})
    
def ask(request):
    return render(request,'ask.html', {})
    
def login(request):
    return render(request,'login.html', {})
    
def signup(request):
    return render(request,'signup.html', {})
    
def settings(request):
    return render(request,'settings.html', {})
    
def default(request):
    return render(request,'index.html', {})

def question_page(request,no):
    question = Question.objects.filter(identificator = no).first()
    answers = Answer.objects.filter(question__identificator = no)
    page_obj = paginate(request, answers)
    return render(request,'question.html', {'question':question,'answers':answers,'page_obj': page_obj})
    
