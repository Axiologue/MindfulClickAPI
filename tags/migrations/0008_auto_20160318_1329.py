# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0007_auto_20160318_1235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethicstag',
            options={'ordering': ('reference', 'tag_type')},
        ),
        migrations.RenameField(
            model_name='ethicstag',
            old_name='article',
            new_name='reference',
        ),
        migrations.RenameField(
            model_name='metatag',
            old_name='article',
            new_name='reference',
        ),
        migrations.AlterUniqueTogether(
            name='metatag',
            unique_together=set([('tag_type', 'reference')]),
        ),
    ]
