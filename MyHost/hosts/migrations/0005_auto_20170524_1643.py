# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-24 08:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0004_auto_20170524_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='business_line',
            new_name='business',
        ),
    ]