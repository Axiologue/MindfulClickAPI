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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tilte', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('owns', models.ForeignKey(to='refData.Company', related_name='parent')),
            ],
        ),
        migrations.CreateModel(
            name='CrossReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.SmallIntegerField(choices=[(-5, '-5'), (-4, '-4'), (-3, '-3'), (-2, '-2'), (-1, '-1'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0)),
                ('article', models.ManyToManyField(related_name='data', to='refData.Article')),
            ],
        ),
        migrations.CreateModel(
            name='EthicsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='EthicsSubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('category', models.ForeignKey(to='refData.EthicsCategory', related_name='subcategories')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('division', models.CharField(max_length=1, null=True, choices=[('M', 'Men'), ('W', 'Women'), ('U', 'Unisex'), ('K', 'Kids'), ('P', 'Preschool'), ('I', 'Infant/Toddler'), ('B', 'Boys'), ('G', 'Girls')], blank=True)),
                ('category', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image_link', models.URLField()),
                ('Company', models.ForeignKey(to='refData.Company', related_name='products')),
            ],
        ),
        migrations.AddField(
            model_name='crossreference',
            name='subcategory',
            field=models.ForeignKey(to='refData.EthicsSubCategory', related_name='data'),
        ),
    ]
