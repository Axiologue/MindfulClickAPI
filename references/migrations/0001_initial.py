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
            name='Reference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(unique=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('pub_date', models.DateTimeField(null=True, blank=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-add_date',),
            },
        ),
    ]
