# Generated by Django 3.1.3 on 2020-11-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_author_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers_count',
            field=models.IntegerField(default=0, verbose_name='количество ответов'),
        ),
    ]
