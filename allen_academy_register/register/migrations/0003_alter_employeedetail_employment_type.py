# Generated by Django 4.2.6 on 2024-12-31 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_alter_registrationkey_year_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetail',
            name='employment_type',
            field=models.CharField(choices=[('T', 'Teacher'), ('A', 'Administrative Staff'), ('S', 'Other Staff'), ('D', 'Dean')], default='T', max_length=1),
        ),
    ]
