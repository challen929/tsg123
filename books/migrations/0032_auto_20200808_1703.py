# Generated by Django 2.2.14 on 2020-08-08 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0031_auto_20200808_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='member',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='books.MemberState'),
        ),
    ]
