# Generated by Django 2.2.14 on 2020-08-07 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0025_purchasedetail_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasebatch',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]