# Generated by Django 3.1.5 on 2021-01-20 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0016_merge_20210111_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.room')),
            ],
            options={
                'verbose_name': 'Bloque de horario',
                'verbose_name_plural': 'Bloques de horarios',
            },
        ),
    ]
