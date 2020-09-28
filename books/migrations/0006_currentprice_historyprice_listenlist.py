# Generated by Django 2.2.14 on 2020-08-01 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20200801_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListenList',
            fields=[
                ('product_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoryPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.BigIntegerField()),
                ('ori_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('daily_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cut_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('plus_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prom', models.CharField(max_length=10)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.ListenList')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurrentPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.BigIntegerField()),
                ('ori_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('daily_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cut_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('plus_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prom', models.CharField(max_length=10)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('pre_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bot_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.ListenList')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
