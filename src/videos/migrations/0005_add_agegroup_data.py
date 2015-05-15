# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.core.management import call_command

def add_agegroup_data(apps, schema_editor):
    call_command('loaddata', 'agegroup_data.json')
    pass


def remove_agegroup_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20150514_1214'),
    ]

    operations = [
        migrations.RunPython(
            add_agegroup_data,
            reverse_code=remove_agegroup_data
        )
    ]
