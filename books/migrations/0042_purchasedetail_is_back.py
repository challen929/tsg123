# Generated by Django 2.2.14 on 2020-08-12 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0041_auto_20200812_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedetail',
            name='is_back',
            field=models.BooleanField(default=0),
        ),
    ]
