# Generated by Django 3.1.5 on 2021-01-20 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0017_speechtime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='speechtime',
            options={'verbose_name': 'Activity Duration', 'verbose_name_plural': 'Activity Duration'},
        ),
        migrations.AddField(
            model_name='speech',
            name='time_asked',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='time_asked', to='proposal.speechtime', verbose_name='Duration'),
        ),
        migrations.AddField(
            model_name='speech',
            name='time_given',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='time_given', to='proposal.speechtime', verbose_name='Duration Assigned'),
        ),
        migrations.AlterField(
            model_name='speechtime',
            name='time',
            field=models.IntegerField(default=10, verbose_name='Time (in minutes)'),
        ),
    ]