# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-02 18:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gustos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, 'Creado usuario'), (1, 'Pre-registo'), (2, 'Confirmado')], default=0)),
                ('identification', models.CharField(max_length=12, null=True, verbose_name='Identificación en su país')),
                ('born_date', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('institution', models.CharField(blank=True, max_length=12, null=True, verbose_name='Institución')),
                ('gender', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], default='Masculino', max_length=9, verbose_name='Género')),
                ('nationality', models.CharField(choices=[('Panamá', 'Panamá'), ('Costa Rica', 'Costa Rica'), ('Nicaragua', 'Nicaragua'), ('El Salvador', 'El salvador'), ('Hondura', 'Honduras'), ('Belize', 'Belize'), ('Otro', 'Otro')], max_length=12, verbose_name='Nacionalidad')),
                ('other_nationality', models.CharField(blank=True, max_length=12, null=True, verbose_name='Indique la Nacionalidad')),
                ('alimentary_restriction', models.TextField(null=True, verbose_name='¿Tiene alguna necesidad específica de alimentación y hospedaje o alguna condición de salud especial?.')),
                ('health_consideration', models.TextField(null=True, verbose_name='Condiciones de Salud')),
                ('comentario_general', models.TextField(null=True, verbose_name='Si tiene algún comentario y/o si quiere colaborar con la organización del 9° ECSL por favor comente en este espacio.')),
                ('gustos_manias', models.ManyToManyField(to='ecsl.Gustos')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Patrocinadores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('web', models.URLField(verbose_name='Web')),
                ('logo', models.ImageField(upload_to='logos/', verbose_name='logo')),
                ('patrocin', models.SmallIntegerField(choices=[('gold', 'Oro'), ('Plate', 'Plata'), ('Bronce', 'Bronce')])),
            ],
            options={
                'verbose_name_plural': 'Patrons',
                'verbose_name': 'Patron',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_de_referencia', models.CharField(help_text='Identificación de transacción o código de referencia', max_length=12, verbose_name='Id de transacción')),
                ('invoice', models.FileField(upload_to='invoices/')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('identification', models.CharField(max_length=12, null=True, verbose_name='Identificación')),
                ('tipo', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecsl.PaymentOption', verbose_name='Usuario'),
        ),
    ]
