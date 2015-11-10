# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile', '0005_auto_20151106_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='modifier',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='applied', blank=True),
        ),
    ]
