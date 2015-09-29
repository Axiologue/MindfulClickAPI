# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0010_auto_20150927_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='add_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 9, 27, 21, 3, 11, 539114, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
