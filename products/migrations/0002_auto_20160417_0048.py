# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='owns',
        ),
        migrations.AddField(
            model_name='company',
            name='owned_by',
            field=models.ForeignKey(related_name='owns', null=True, blank=True, to='products.Company'),
        ),
    ]
