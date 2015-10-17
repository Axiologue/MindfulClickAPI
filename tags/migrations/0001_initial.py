# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('refData', '0015_auto_20151016_1804'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EthicsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EthicsSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('category', models.ForeignKey(to='tags.EthicsCategory', related_name='subcategories')),
            ],
            options={
                'ordering': ('category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='EthicsTag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('excerpt', models.TextField()),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(to='refData.Article', related_name='ethicstag')),
                ('company', models.ForeignKey(to='refData.Company', related_name='tags')),
                ('product', models.ForeignKey(blank=True, to='refData.Product', related_name='tags', null=True)),
            ],
            options={
                'ordering': ('article', 'tag_type'),
            },
        ),
        migrations.CreateModel(
            name='EthicsType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('subcategory', models.ForeignKey(to='tags.EthicsSubCategory', related_name='tag_types')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(to='refData.Article', related_name='metatag')),
            ],
        ),
        migrations.CreateModel(
            name='MetaType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='metatag',
            name='tag_type',
            field=models.ForeignKey(to='tags.MetaType'),
        ),
        migrations.AddField(
            model_name='ethicstag',
            name='tag_type',
            field=models.ForeignKey(to='tags.EthicsType'),
        ),
        migrations.AlterUniqueTogether(
            name='metatag',
            unique_together=set([('tag_type', 'article')]),
        ),
        migrations.AlterUniqueTogether(
            name='ethicstag',
            unique_together=set([('tag_type', 'article', 'company')]),
        ),
    ]
