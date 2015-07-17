# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(unique=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('owns', models.ForeignKey(to='refData.Company', related_name='parent', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrossReference',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('score', models.SmallIntegerField(choices=[(-5, '-5'), (-4, '-4'), (-3, '-3'), (-2, '-2'), (-1, '-1'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0)),
                ('notes', models.TextField(blank=True, null=True)),
                ('article', models.ForeignKey(related_name='data', to='refData.Article')),
                ('company', models.ForeignKey(to='refData.Company', related_name='data', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthicsCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthicsSubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('category', models.ForeignKey(related_name='subcategories', to='refData.EthicsCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('division', models.CharField(max_length=30, blank=True, null=True)),
                ('category', models.CharField(max_length=40, blank=True, null=True)),
                ('price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('image_link', models.URLField()),
                ('company', models.ForeignKey(related_name='products', to='refData.Company')),
            ],
        ),
        migrations.AddField(
            model_name='crossreference',
            name='product',
            field=models.ForeignKey(to='refData.Product', related_name='data', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='crossreference',
            name='subcategory',
            field=models.ForeignKey(related_name='data', to='refData.EthicsSubCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'division')]),
        ),
    ]
