# Generated by Django 3.1.2 on 2020-11-10 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0009_auto_20201110_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='client',
            name='price',
        ),
        migrations.RemoveField(
            model_name='client',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='client',
            name='receipt',
        ),
        migrations.RemoveField(
            model_name='client',
            name='recurring',
        ),
    ]