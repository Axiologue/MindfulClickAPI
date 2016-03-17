# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0007_auto_20150918_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagtype',
            name='subcategory',
            field=models.ForeignKey(related_name='tag_types', to='references.EthicsSubCategory'),
        ),
    ]
