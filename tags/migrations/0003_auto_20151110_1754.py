# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20151016_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethicstag',
            name='company',
            field=models.ForeignKey(null=True, to='references.Company', related_name='tags', blank=True),
        ),
    ]
