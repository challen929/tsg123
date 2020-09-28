# Generated by Django 2.2.14 on 2020-08-11 10:55

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0035_auto_20200811_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberstate',
            name='age_of_boy',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='age_of_girl',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]