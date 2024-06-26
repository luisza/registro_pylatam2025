# Generated by Django 3.1.5 on 2021-01-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0034_merge_20210111_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventecsl',
            name='oganizer1',
            field=models.CharField(max_length=25, null=True, verbose_name='First organizer'),
        ),
        migrations.AddField(
            model_name='eventecsl',
            name='oganizer2',
            field=models.CharField(max_length=25, null=True, verbose_name='Second organizer'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start Date'),
        ),
    ]
