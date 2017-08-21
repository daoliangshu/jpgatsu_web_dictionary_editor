# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-14 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('db_editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionaryentry',
            name='en_1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='fr_1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='fr_2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='jp_1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='jp_2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='lesson',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='lv',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='thematic',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dictionaryentry',
            name='zh_1',
            field=models.CharField(max_length=255, null=True),
        ),
    ]