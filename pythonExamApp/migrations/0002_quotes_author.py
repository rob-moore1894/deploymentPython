# Generated by Django 2.2.4 on 2020-08-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonExamApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='author',
            field=models.CharField(default='Anonymous', max_length=255),
        ),
    ]
