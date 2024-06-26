# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-05 06:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecsl', '0008_inscription_observacion_gustos_manias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Becas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon', models.TextField(verbose_name='Dinos porqué deberíamos darte la beca')),
                ('aportes_a_la_comunidad', models.TextField(verbose_name='¿Cúales son tus aportes a la comunidad ?')),
                ('tiempo', models.CharField(max_length=250, verbose_name='Tiempo involucrado/a en el Software Libre, ej 2 años')),
                ('observaciones', models.TextField(verbose_name='¿Alguna observación adicional?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
