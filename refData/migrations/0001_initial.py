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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(unique=True)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('owns', models.ForeignKey(related_name='parent', to='refData.Company', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrossReference',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('score', models.SmallIntegerField(default=0, choices=[(-5, '-5'), (-4, '-4'), (-3, '-3'), (-2, '-2'), (-1, '-1'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('notes', models.TextField(null=True, blank=True)),
                ('article', models.ManyToManyField(to='refData.Article', related_name='data')),
            ],
        ),
        migrations.CreateModel(
            name='EthicsCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthicsSubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('category', models.ForeignKey(to='refData.EthicsCategory', related_name='subcategories')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('division', models.CharField(null=True, max_length=30, blank=True)),
                ('category', models.CharField(null=True, max_length=40, blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image_link', models.URLField()),
                ('company', models.ForeignKey(to='refData.Company', related_name='products')),
            ],
        ),
        migrations.AddField(
            model_name='crossreference',
            name='subcategory',
            field=models.ForeignKey(to='refData.EthicsSubCategory', related_name='data'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'division')]),
        ),
    ]
