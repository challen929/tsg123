# Generated by Django 2.2.14 on 2020-08-14 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0051_memberlog_paid_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(max_length=16)),
                ('ISBN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
            ],
            options={
                'unique_together': {('package_id', 'ISBN')},
            },
        ),
    ]
