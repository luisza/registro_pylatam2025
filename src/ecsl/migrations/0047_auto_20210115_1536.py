# Generated by Django 3.1.5 on 2021-01-15 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0046_merge_20210114_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventecsl',
            name='end_date_proposal',
            field=models.DateField(blank=True, null=True, verbose_name='End Date Proposal'),
        ),
        migrations.AlterField(
            model_name='eventecsl',
            name='start_date_proposal',
            field=models.DateField(blank=True, null=True, verbose_name='Start Date Proposal'),
        ),
    ]