# Generated by Django 3.1.5 on 2021-01-08 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0025_auto_20210107_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventecsl',
            name='logo',
            field=models.ImageField(default='static/img/logos/RanaCirculo.png', max_length=50, null=True, upload_to='img/logos/'),
        ),
    ]
