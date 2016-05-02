# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='choice',
            name='key',
            field=models.CharField(default='key', max_length=50, verbose_name='Value'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='condition',
            name='related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='condition_related', to='questions.Question', verbose_name='Related'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condition_target', to='questions.Question', verbose_name='Target'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='type',
            field=models.CharField(choices=[(b'is-true', 'Is true'), (b'is-false', 'Is false'), (b'is-equal', 'Is equal'), (b'is-not-equal', 'Is not equal')], default=b'is-true', max_length=15, verbose_name='Answer type'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[(b'short_text', 'Short text answer'), (b'long_text', 'Long text answer'), (b'choice', 'Choice answer')], default=b'short_text', max_length=25, verbose_name='Answer type'),
        ),
    ]
