# Generated by Django 3.1.5 on 2021-02-11 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0029_merge_20210126_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speech',
            name='speech_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.speechtype', verbose_name='Speech Types'),
        ),
    ]