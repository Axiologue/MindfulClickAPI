# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_auto_20160331_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='axiologueuser',
            old_name='preferences_new',
            new_name='preferences',
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('preference', 'tag_type')]),
        ),
        migrations.RemoveField(
            model_name='preference',
            name='user',
        ),
    ]
