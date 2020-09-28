# Generated by Django 2.2.14 on 2020-07-31 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4)),
                ('days', models.IntegerField()),
                ('price', models.IntegerField()),
                ('discount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MemberState',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('deposit', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=10, null=True)),
                ('parent', models.CharField(max_length=4, null=True)),
                ('age_of_boy', models.IntegerField(null=True)),
                ('age_of_girl', models.IntegerField(null=True)),
                ('memo', models.CharField(max_length=50, null=True)),
                ('referer', models.IntegerField(default=1000)),
                ('state', models.IntegerField()),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.Member')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.MemberType')),
            ],
        ),
    ]