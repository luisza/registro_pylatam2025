# Generated by Django 3.1.5 on 2021-01-12 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0038_eventecsl_phone_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventecsl',
            name='proposal_period',
            field=models.BooleanField(default=False, verbose_name='Proposal Period'),
        ),
    ]
