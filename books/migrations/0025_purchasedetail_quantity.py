# Generated by Django 2.2.14 on 2020-08-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_purchasedetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedetail',
            name='quantity',
            field=models.SmallIntegerField(default=1),
        ),
    ]