# Generated by Django 3.1.5 on 2021-01-07 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsl', '0024_auto_20210107_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventecsl',
            name='logo',
            field=models.ImageField(default='img/logos/RanaCirculo.png', max_length=50, null=True, upload_to='img/logos/'),
        ),
    ]
