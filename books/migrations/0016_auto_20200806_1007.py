# Generated by Django 2.2.14 on 2020-08-06 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_auto_20200804_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowrecord',
            old_name='borrow_memo',
            new_name='memo',
        ),
        migrations.RemoveField(
            model_name='borrowrecord',
            name='return_memo',
        ),
    ]
