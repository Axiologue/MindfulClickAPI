# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20151016_1920'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile', '0002_auto_20151106_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('preference', models.FloatField()),
                ('tag_type', models.ForeignKey(to='tags.EthicsType')),
                ('user', models.ForeignKey(related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tagpref',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tagpref',
            name='tag_type',
        ),
        migrations.RemoveField(
            model_name='tagpref',
            name='user',
        ),
        migrations.DeleteModel(
            name='TagPref',
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('user', 'tag_type')]),
        ),
    ]
