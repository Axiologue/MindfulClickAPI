# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_answer_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='answered', blank=True),
        ),
    ]
