# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpmpb', '0003_auto_20170710_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miniature',
            name='description',
            field=models.CharField(blank=True, default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='miniature',
            name='tags',
            field=models.ManyToManyField(blank=True, to='rpmpb.Tag'),
        ),
        migrations.AlterField(
            model_name='photosession',
            name='description',
            field=models.CharField(blank=True, default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='photosession',
            name='tags',
            field=models.ManyToManyField(blank=True, to='rpmpb.Tag'),
        ),
        migrations.AlterField(
            model_name='photosession',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]