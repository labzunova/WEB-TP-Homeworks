from django.db import models
from django.utils import timezone

class Author(models.Model):
    #avatar = 

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class User(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    
class Tag(models.Model):
    title = models.TextField(null=True, verbose_name='Тег')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
class QuestionManager(models.Manager):
    def best_questions(self):
        return self.order_by('-rating')
      
    def new_questions(self):
        return self.order_by('-date_create')

    class Meta:
        verbose_name = 'User'
        
class Question(models.Model):
    identificator = models.IntegerField(verbose_name='id вопроса', default=0)
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
       
        
class Answer(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True,  verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,  verbose_name='Вопрос')
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    is_right = models.BooleanField(default=False, verbose_name='Правильность')
    text = models.TextField(null=True, verbose_name='Текст')
	
    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Article(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        
# Create your models here.
