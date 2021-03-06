# Generated by Django 3.1.2 on 2020-10-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('problem', models.CharField(max_length=64)),
                ('notes', models.CharField(max_length=1000)),
                ('session_number', models.IntegerField()),
                ('recurring', models.BooleanField()),
                ('price', models.IntegerField()),
                ('receipt', models.BooleanField()),
                ('email', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
            ],
        ),
    ]
