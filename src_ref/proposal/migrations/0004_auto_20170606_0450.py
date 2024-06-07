# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 04:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposal', '0003_auto_20170605_0612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register_Speech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('spaces', models.SmallIntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='SpeechSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.Room')),
                ('speech', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.Speech')),
            ],
        ),
        migrations.AddField(
            model_name='register_speech',
            name='speech',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.SpeechSchedule'),
        ),
        migrations.AddField(
            model_name='register_speech',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]