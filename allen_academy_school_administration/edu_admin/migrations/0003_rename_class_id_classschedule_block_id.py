# Generated by Django 4.2.6 on 2024-06-22 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edu_admin', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classschedule',
            old_name='class_id',
            new_name='block_id',
        ),
    ]
