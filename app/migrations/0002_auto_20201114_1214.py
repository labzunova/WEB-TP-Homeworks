# Generated by Django 3.1.3 on 2020-11-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='identificator',
            field=models.IntegerField(default=0, verbose_name='id вопроса'),
        ),
    ]
