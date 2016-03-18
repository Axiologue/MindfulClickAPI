# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0018_auto_20160318_1402')
    ]

    state_operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('owns', models.ForeignKey(blank=True, related_name='parent', to='products.Company', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('division', models.CharField(blank=True, null=True, max_length=30)),
                ('category', models.CharField(blank=True, null=True, max_length=40)),
                ('price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('image_link', models.URLField(blank=True, null=True, max_length=350)),
                ('company', models.ForeignKey(to='products.Company', related_name='products')),
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

    operations = [
        # By running only state operations, we are making Django think it has
        # applied this migration to the database. In reality, we renamed a
        # "cars_tires" table to "tires_tires" earlier.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
