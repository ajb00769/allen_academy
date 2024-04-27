# Generated by Django 4.2.6 on 2024-04-26 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('register', '0005_alter_allaccount_email_alter_allaccount_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allaccount',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. Users are granted permissions relative to the groups they belong to', related_name='common_user_groups', to='auth.group', verbose_name='common user groups'),
        ),
        migrations.AlterField(
            model_name='allaccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific user permissions.', related_name='common_user_permissions', to='auth.permission', verbose_name='common user permissions'),
        ),
    ]
