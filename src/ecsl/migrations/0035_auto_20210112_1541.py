# Generated by Django 3.1.5 on 2021-01-12 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0034_merge_20210111_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventecsl',
            name='beca_end',
            field=models.DateField(null=True, verbose_name='Scholarship application end date'),
        ),
        migrations.AddField(
            model_name='eventecsl',
            name='beca_start',
            field=models.DateField(null=True, verbose_name='Scholarship application start date'),
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
