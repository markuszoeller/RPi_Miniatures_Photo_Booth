# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpmpb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_name', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='photosession',
            name='description',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='miniature',
            name='description',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='miniature',
            name='name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=models.ManyToManyField(to='rpmpb.Tag'),
        ),
        migrations.AddField(
            model_name='miniature',
            name='tags',
            field=models.ManyToManyField(to='rpmpb.Tag'),
        ),
        migrations.AddField(
            model_name='photosession',
            name='tags',
            field=models.ManyToManyField(to='rpmpb.Tag'),
        ),
    ]