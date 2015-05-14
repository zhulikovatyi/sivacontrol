# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20150421_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_boundary', models.IntegerField()),
                ('stop_boundary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BannerWeight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(choices=[(0, b'Too Low'), (1, b'Low'), (2, b'Middle'), (3, b'High')])),
                ('age_group', models.ForeignKey(to='videos.AgeGroup')),
            ],
        ),
        migrations.RemoveField(
            model_name='banner',
            name='genders',
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(default=b'Coming soon ...', max_length=256),
        ),
        migrations.AddField(
            model_name='bannerweight',
            name='banner',
            field=models.ForeignKey(related_name='age_gender_weights', to='videos.Banner'),
        ),
        migrations.AddField(
            model_name='bannerweight',
            name='gender',
            field=models.ForeignKey(to='videos.Gender'),
        ),
    ]
