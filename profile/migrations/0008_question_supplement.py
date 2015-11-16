# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_auto_20151106_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='supplement',
            field=models.TextField(null=True, blank=True),
        ),
    ]
