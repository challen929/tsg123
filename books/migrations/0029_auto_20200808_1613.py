# Generated by Django 2.2.14 on 2020-08-08 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0028_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='books.Book'),
        ),
    ]
