# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0009_auto_20150920_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='company',
            field=models.ForeignKey(related_name='tags', to='refData.Company', default=1),
            preserve_default=False,
        ),
    ]
