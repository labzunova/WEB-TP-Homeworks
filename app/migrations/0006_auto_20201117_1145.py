# Generated by Django 3.1.3 on 2020-11-17 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201117_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='author',
            new_name='user',
        ),
    ]