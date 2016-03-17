# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_auto_20151110_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethicstag',
            name='company',
            field=models.ForeignKey(related_name='tags', to='references.Company', default=1),
            preserve_default=False,
        ),
    ]
