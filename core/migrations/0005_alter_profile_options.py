# Generated by Django 4.1.2 on 2022-10-19 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_profile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('view_student', 'Can view Student Page'), ('view_admin', 'Can view admin Page'), ('view_staff', 'Can view staff Page'), ('view_editor', 'Can view editor Page'))},
        ),
    ]
