# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('references', '0003_auto_20150908_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactoidType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('subcategory', models.ForeignKey(to='references.EthicsSubCategory', related_name='factoids')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('excerpt', models.TextField()),
                ('value', models.IntegerField(null=True, blank=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(to='references.Article', related_name='tags')),
                ('company', models.ForeignKey(null=True, blank=True, to='references.Company', related_name='tags')),
                ('fact_type', models.ForeignKey(to='references.FactoidType')),
                ('product', models.ForeignKey(null=True, blank=True, to='references.Product', related_name='tags')),
                ('submited_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='factoid',
            name='article',
        ),
        migrations.RemoveField(
            model_name='factoid',
            name='company',
        ),
        migrations.RemoveField(
            model_name='factoid',
            name='product',
        ),
        migrations.RemoveField(
            model_name='factoid',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Factoid',
        ),
    ]
