# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 13:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_auto_20170613_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendshipstatus',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='friendshipstatus',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='FriendshipStatus',
        ),
    ]
