# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=50)),
                ('owns', models.ForeignKey(related_name='parent', null=True, to='products.Company', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('division', models.CharField(max_length=30, null=True, blank=True)),
                ('category', models.CharField(max_length=40, null=True, blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image_link', models.URLField(max_length=350, null=True, blank=True)),
                ('company', models.ForeignKey(related_name='products', to='products.Company')),
            ],
            options={
                'ordering': ('company', 'name'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'division')]),
        ),
    ]
