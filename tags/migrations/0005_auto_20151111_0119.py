# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_auto_20151111_0047'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ethicstag',
            unique_together=set([('tag_type', 'article', 'company', 'product')]),
        ),
    ]
