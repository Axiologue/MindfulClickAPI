# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0014_article_added_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ethicssubcategory',
            name='category',
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tag',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='article',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='company',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='product',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tag_type',
        ),
        migrations.RemoveField(
            model_name='tagtype',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='EthicsCategory',
        ),
        migrations.DeleteModel(
            name='EthicsSubCategory',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='TagType',
        ),
    ]
