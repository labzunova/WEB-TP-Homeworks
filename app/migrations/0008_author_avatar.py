# Generated by Django 3.1.3 on 2020-11-17 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_user_identificator'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='avatar',
            field=models.ImageField(default='askсats/static/images/test.jpg', upload_to=''),
        ),
    ]
