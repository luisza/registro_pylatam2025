# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-02 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0003_auto_20170602_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='confirmado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paquete',
            field=models.CharField(choices=[('Completo', 'Completo (Habitación compartida en hostal - Alimentación - Ingreso a actividades)'), ('Sin hotel', 'Sin hotel (Acceso a actividades - Alimentación)')], max_length=40),
        ),
    ]