# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=300, unique=True)),
                ('sub_title', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('title_url', models.SlugField(editable=False)),
                ('posted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pub_time'],
            },
        ),
    ]
