# Generated by Django 2.2.14 on 2020-08-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_borrowrecord_update_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='plus_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='sell_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]