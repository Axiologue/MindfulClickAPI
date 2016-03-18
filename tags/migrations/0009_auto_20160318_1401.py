# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0008_auto_20160318_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethicstag',
            name='company',
            field=models.ForeignKey(to='products.Company', related_name='tags'),
        ),
        migrations.AlterField(
            model_name='ethicstag',
            name='product',
            field=models.ForeignKey(to='products.Product', related_name='tags', null=True, blank=True),
        ),
    ]
