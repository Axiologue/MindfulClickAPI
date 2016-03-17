# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0002_auto_20150811_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factoid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fact_type', models.CharField(max_length=300)),
                ('value', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('article', models.ForeignKey(related_name='factoids', to='references.Article')),
                ('company', models.ForeignKey(blank=True, to='references.Company', related_name='factoids', null=True)),
                ('product', models.ForeignKey(blank=True, to='references.Product', related_name='factoids', null=True)),
                ('subcategory', models.ForeignKey(related_name='factoids', to='references.EthicsSubCategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='crossreference',
            name='article',
        ),
        migrations.RemoveField(
            model_name='crossreference',
            name='company',
        ),
        migrations.RemoveField(
            model_name='crossreference',
            name='product',
        ),
        migrations.RemoveField(
            model_name='crossreference',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='CrossReference',
        ),
    ]
