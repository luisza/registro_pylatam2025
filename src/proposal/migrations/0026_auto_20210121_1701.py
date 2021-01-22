# Generated by Django 3.1.5 on 2021-01-21 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0025_auto_20210121_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialactivity',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='specialactivity',
            name='start_time',
        ),
        migrations.AddField(
            model_name='specialactivity',
            name='time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='proposal.speechtime', verbose_name='Duration Assigned'),
        ),
    ]
