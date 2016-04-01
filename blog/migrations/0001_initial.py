# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(unique=True, max_length=300)),
                ('sub_title', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('title_url', models.SlugField(editable=False)),
            ],
            options={
                'ordering': ['-pub_time'],
            },
        ),
    ]
