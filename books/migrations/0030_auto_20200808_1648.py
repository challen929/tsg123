# Generated by Django 2.2.14 on 2020-08-08 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0029_auto_20200808_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='member',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='books.MemberState'),
        ),
    ]
