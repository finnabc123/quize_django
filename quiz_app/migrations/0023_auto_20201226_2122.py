# Generated by Django 3.1.4 on 2020-12-27 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0022_quiz_quiz_negative_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiz_negative_point',
            field=models.IntegerField(default=0),
        ),
    ]
