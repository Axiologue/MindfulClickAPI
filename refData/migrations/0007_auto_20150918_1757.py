# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0006_auto_20150918_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='fact_type',
            new_name='tag_type',
        ),
    ]
