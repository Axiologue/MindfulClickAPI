# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0008_auto_20150918_1926'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('tag_type', 'article', 'company')]),
        ),
    ]
