# Generated by Django 2.2.14 on 2020-08-18 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0054_auto_20200815_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='placed_on',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stocked_on',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
