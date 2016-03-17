# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0011_auto_20150927_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('add_date',)},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='ethicscategory',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='ethicssubcategory',
            options={'ordering': ('category', 'name')},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('company', 'name')},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('article', 'tag_type')},
        ),
        migrations.AlterModelOptions(
            name='tagtype',
            options={'ordering': ('name',)},
        ),
    ]
