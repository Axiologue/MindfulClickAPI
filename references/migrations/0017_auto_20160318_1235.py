# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0007_auto_20160318_1235'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('references', '0016_auto_20151201_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(unique=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('add_date',),
            },
        ),
        migrations.RemoveField(
            model_name='article',
            name='added_by',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
