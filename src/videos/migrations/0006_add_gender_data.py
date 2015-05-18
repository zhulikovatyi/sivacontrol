# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.core.management import call_command

def add_gender_data(apps, schema_editor):
    call_command('loaddata', 'gender_data.json')
    pass


def remove_gender_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_gender_data,
            reverse_code=remove_gender_data
        )
    ]
