# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='tag_type',
            field=models.ForeignKey(to='tags.EthicsType'),
        ),
        migrations.AddField(
            model_name='preference',
            name='user',
            field=models.ForeignKey(related_name='preferences_old', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='modifier',
            name='answer',
            field=models.ForeignKey(related_name='modifiers', to='profile.Answer'),
        ),
        migrations.AddField(
            model_name='modifier',
            name='tag_type',
            field=models.ForeignKey(to='tags.EthicsType'),
        ),
        migrations.AddField(
            model_name='modifier',
            name='users',
            field=models.ManyToManyField(related_name='applied', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='profile.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='users',
            field=models.ManyToManyField(related_name='answered', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='axiologueuser',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', related_name='user_set', blank=True, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='axiologueuser',
            name='preferences',
            field=models.ManyToManyField(related_name='users', to='profile.Preference'),
        ),
        migrations.AddField(
            model_name='axiologueuser',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', help_text='Specific permissions for this user.', related_query_name='user', related_name='user_set', blank=True, to='auth.Permission'),
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('user', 'tag_type')]),
        ),
    ]
