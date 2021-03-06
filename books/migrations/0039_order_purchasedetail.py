# Generated by Django 2.2.14 on 2020-08-11 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0038_auto_20200811_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISBN', models.CharField(max_length=16)),
                ('package_id', models.CharField(max_length=16)),
                ('price_sale', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price_paid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quantity', models.SmallIntegerField(default=1)),
                ('is_sold', models.BooleanField(default=0)),
                ('memo', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.PurchaseBatch')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('actually_paid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='books.MemberState')),
                ('purchase', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='books.PurchaseDetail')),
            ],
        ),
    ]
