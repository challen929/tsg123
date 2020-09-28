# Generated by Django 2.2.14 on 2020-07-31 10:20

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_memberstate_membertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberstate',
            name='age_of_boy',
            field=models.CharField(max_length=3, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='age_of_girl',
            field=models.CharField(max_length=3, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='deposit',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='state',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='membertype',
            name='days',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='membertype',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
        migrations.AlterField(
            model_name='membertype',
            name='price',
            field=models.SmallIntegerField(),
        ),
    ]
