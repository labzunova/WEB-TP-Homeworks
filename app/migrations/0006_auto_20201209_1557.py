# Generated by Django 3.1.3 on 2020-12-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201209_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(default='test.jpg', upload_to='avatar/%Y/%m/%d/', verbose_name='avatar'),
        ),
    ]