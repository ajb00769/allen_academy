# Generated by Django 4.2.6 on 2024-04-06 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_studentdetail_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetail',
            name='middle_name',
            field=models.CharField(default=None, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='parentdetail',
            name='middle_name',
            field=models.CharField(default=None, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='studentdetail',
            name='middle_name',
            field=models.CharField(default=None, max_length=80, null=True),
        ),
    ]