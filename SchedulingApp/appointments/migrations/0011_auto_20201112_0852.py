# Generated by Django 3.1.2 on 2020-11-12 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0010_auto_20201110_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='recurring',
        ),
        migrations.AddField(
            model_name='client',
            name='problem',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='recurring',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='session_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
