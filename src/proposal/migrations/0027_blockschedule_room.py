# Generated by Django 3.1.5 on 2021-01-23 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0026_auto_20210121_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockschedule',
            name='room',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='proposal.room', verbose_name='Room'),
        ),
    ]
