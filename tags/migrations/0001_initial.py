# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('references', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EthicsCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EthicsSubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('category', models.ForeignKey(related_name='subcategories', to='tags.EthicsCategory')),
            ],
            options={
                'ordering': ('category', 'name'),
            },
        ),
        migrations.CreateModel(
            name='EthicsTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('excerpt', models.TextField()),
                ('value', models.DecimalField(decimal_places=2, null=True, max_digits=15, blank=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(related_name='tags', to='products.Company')),
                ('product', models.ForeignKey(related_name='tags', null=True, to='products.Product', blank=True)),
                ('reference', models.ForeignKey(related_name='ethicstags', to='references.Reference')),
            ],
            options={
                'ordering': ('reference', 'tag_type'),
            },
        ),
        migrations.CreateModel(
            name='EthicsType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('subcategory', models.ForeignKey(related_name='tag_types', to='tags.EthicsSubCategory')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('reference', models.ForeignKey(related_name='metatags', to='references.Reference')),
            ],
        ),
        migrations.CreateModel(
            name='MetaType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
            unique_together=set([('tag_type', 'reference')]),
        ),
    ]
