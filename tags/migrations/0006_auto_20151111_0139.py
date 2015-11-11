# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0005_auto_20151111_0119'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ethicstag',
            unique_together=set([]),
        ),
    ]
