# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('street_address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=75)),
                ('postal_code', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(to='events.Location'),
        ),
    ]
