# Generated by Django 2.2.14 on 2020-07-31 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
