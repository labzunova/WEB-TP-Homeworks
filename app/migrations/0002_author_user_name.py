# Generated by Django 3.1.3 on 2020-11-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='user_name',
            field=models.CharField(default='null', max_length=256, verbose_name='Имя в системе'),
        ),
    ]
