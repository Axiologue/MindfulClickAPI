# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0017_auto_20160318_1235'),
    ]

    # Add custom database_operations
    database_operations = [
        # You have to use Django's database table naming defaults to get the 
        # name 'tires_tires'. It is basically <app_name>_<model_name>.
        migrations.AlterModelTable('product', 'products_product'), 
        migrations.AlterModelTable('company', 'products_company'), 
    ]

    # Don't modify the Django 'state' yet
    state_operations = [

    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]