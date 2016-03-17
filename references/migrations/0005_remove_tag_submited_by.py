# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0004_auto_20150918_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='submited_by',
        ),
    ]
