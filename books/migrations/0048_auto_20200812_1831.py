# Generated by Django 2.2.14 on 2020-08-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0047_auto_20200812_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrecord',
            name='created_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='update_time',
            field=models.DateTimeField(),
        ),
    ]
