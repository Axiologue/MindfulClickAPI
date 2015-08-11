# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_link',
            field=models.URLField(max_length=350),
        ),
    ]
