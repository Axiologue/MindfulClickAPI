# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0019_auto_20160318_1401'),
    ]

    
    # This needs to be a state-only operation because the database model was
    # renamed, and no longer exists according to Django.
    state_operations = [
        # Pasted from auto-generated operations in previous step:
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]

    operations = [
        # After this state operation, the Django DB state should match the 
        # actual database structure.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
