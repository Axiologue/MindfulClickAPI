# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0005_remove_tag_submited_by'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FactoidType',
            new_name='TagType',
        ),
    ]
