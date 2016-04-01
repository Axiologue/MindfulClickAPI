# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_auto_20160331_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='axiologueuser',
            name='preferences',
        ),
        migrations.AddField(
            model_name='preference',
            name='user',
            field=models.ForeignKey(related_name='preferences', to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('user', 'tag_type')]),
        ),
    ]
