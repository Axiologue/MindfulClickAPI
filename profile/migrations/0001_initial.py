# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0002_auto_20151016_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagPref',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('preference', models.FloatField()),
                ('tag_type', models.ForeignKey(to='tags.EthicsType')),
                ('user', models.ForeignKey(related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tagpref',
            unique_together=set([('user', 'tag_type')]),
        ),
    ]
