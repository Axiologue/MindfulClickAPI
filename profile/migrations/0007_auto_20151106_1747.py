# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_modifier_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modifier',
            old_name='user',
            new_name='users',
        ),
    ]
