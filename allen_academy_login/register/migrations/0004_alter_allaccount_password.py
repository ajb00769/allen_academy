# Generated by Django 4.2.6 on 2024-04-26 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_employeedetail_registrationkey_studentdetail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allaccount',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
