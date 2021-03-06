# Generated by Django 3.1.2 on 2020-11-07 12:05

from django.db import migrations

def assign_user_to_appointments(apps, schema_editor):
    Appointment = apps.get_model('appointments', 'Appointment')
    User = apps.get_model('auth', 'User')
    u = User.objects.filter(username='testuser')
    if u.count() == 0:
        u = User.objects.create_user(username='testuser',email='user@user.ro',password='fwifjie&^*^3333')
    else:
        u = u[0]
    for appointment in Appointment.objects.all():
        appointment.user = u
        appointment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_appointment_user'),
        ('auth', '0012_alter_user_first_name_max_length')
    ]

    operations = [
        migrations.RunPython(assign_user_to_appointments)
    ]
