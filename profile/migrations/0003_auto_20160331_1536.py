# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20160331_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='axiologueuser',
            name='preferences',
        ),
        migrations.AddField(
            model_name='axiologueuser',
            name='preferences_new',
            field=models.ManyToManyField(related_name='users', null=True, blank=True, to='profile.Preference'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='preferences'),
        ),
    ]
