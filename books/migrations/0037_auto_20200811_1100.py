# Generated by Django 2.2.14 on 2020-08-11 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0036_auto_20200811_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created_time',
            field=models.DateTimeField(),
        ),
    ]