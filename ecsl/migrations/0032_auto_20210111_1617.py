# Generated by Django 3.1.5 on 2021-01-11 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0031_auto_20210111_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='becas',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecsl.eventecsl', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='current',
            field=models.BooleanField(default=False, verbose_name='Current'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='description',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='location',
            field=models.CharField(max_length=50, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecsl.eventecsl', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='patrocinadores',
            name='event',
            field=models.ManyToManyField(to='ecsl.EventECSL', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecsl.eventecsl', verbose_name='Event'),
        ),
    ]
