# Generated by Django 3.1.5 on 2021-01-12 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0036_auto_20210112_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventecsl',
            name='certificate_Footer',
            field=models.ImageField(blank=True, null=True, upload_to='img/logos/', verbose_name='Logo'),
        ),
        migrations.AddField(
            model_name='eventecsl',
            name='certificate_Header',
            field=models.ImageField(blank=True, null=True, upload_to='img/logos/', verbose_name='Logo'),
        ),
    ]
