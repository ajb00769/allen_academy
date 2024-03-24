# Generated by Django 4.2.6 on 2024-03-24 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetail',
            name='suffix',
            field=models.CharField(choices=[('JR', 'Junior'), ('SR', 'Senior'), ('II', 'The second'), ('III', 'The third'), ('IV', 'The fourth'), ('V', 'The fifth')], max_length=3, null=True),
        ),
    ]
