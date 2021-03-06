# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 00:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitorings', '0008_auto_20160509_0031'),
        ('questions', '0015_auto_20160505_1201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sheet',
            options={'ordering': ['monitoring_institution', 'user', 'created'], 'verbose_name': 'Sheet', 'verbose_name_plural': 'Sheets'},
        ),
        migrations.AddField(
            model_name='sheet',
            name='monitoring_institution',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monitorings.MonitoringInstitution'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='sheet',
            unique_together=set([('monitoring_institution', 'user')]),
        ),
        migrations.RemoveField(
            model_name='sheet',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='sheet',
            name='monitoring',
        ),

    ]
