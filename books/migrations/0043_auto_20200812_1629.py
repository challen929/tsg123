# Generated by Django 2.2.14 on 2020-08-12 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0042_purchasedetail_is_back'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasebatch',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
