# Generated by Django 3.1.4 on 2020-12-22 10:58

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0006_remove_response_ispaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiz_slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=models.CharField(max_length=256)),
        ),
    ]
