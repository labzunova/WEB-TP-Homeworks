from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


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
