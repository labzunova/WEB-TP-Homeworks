from django.shortcuts import render
import random
from django.core.paginator import Paginator
from app.models import Question

def paginate(request, object_list, per_page=5):
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
    
questions = [
    {
        'id': idx,
        'title':f'question number {idx}',
        'text':'give me an answer!',
        'number_of_answers':f'{10-idx}',
        'users_rating':random.randint(1,100),
        'tags':random.choice(['food', 'paws', 'everyday', 'humans'])
    } for idx in range(10)
]

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
    questions_ = questions.best_questions()
    new = []
    for i in range(10):
    	if questions_[i]['tags'] == tag:
    	    new.append(questions[i])
    paginate(request, new)
    return render(request,'index.html', {'questions':new})
    
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
    question = questions[no]
    page_obj = paginate(request, answers)
    return render(request,'question.html', {'question':question,'answers':answers,'page_obj': page_obj})
    
