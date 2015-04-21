# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20150415_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
