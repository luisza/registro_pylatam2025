# Generated by Django 3.1.5 on 2021-01-15 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0046_merge_20210114_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventecsl',
            name='beca_end',
            field=models.DateField(blank=True, null=True, verbose_name='Scholarship application end period'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='beca_start',
            field=models.DateField(blank=True, null=True, verbose_name='Scholarship application start period'),
        ),
    ]
