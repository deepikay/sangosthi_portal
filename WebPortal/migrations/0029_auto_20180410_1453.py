# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-10 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebPortal', '0028_auto_20180410_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='answer_1',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='answer1_audio', to='WebPortal.AudioFile'),
        ),
        migrations.AlterField(
            model_name='show',
            name='question_1',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='question1_audio', to='WebPortal.AudioFile'),
        ),
    ]