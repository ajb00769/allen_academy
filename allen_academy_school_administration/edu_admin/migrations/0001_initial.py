# Generated by Django 4.2.6 on 2024-06-16 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0008_alter_employeedetail_employment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('course_name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('total_units', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('subject_type', models.CharField(choices=[('M', 'Major'), ('m', 'Minor'), ('E', 'Elective')])),
                ('subject_name', models.CharField(max_length=255)),
                ('subject_units', models.IntegerField()),
                ('wk_class_dura', models.IntegerField()),
                ('subject_tuition', models.FloatField()),
                ('course_yr_lvl', models.CharField(choices=[('EMS1', 'Elementary School 1'), ('EMS2', 'Elementary School 2'), ('EMS3', 'Elementary School 3'), ('EMS4', 'Elementary School 4'), ('EMS5', 'Elementary School 5'), ('EMS6', 'Elementary School 6'), ('MDS1', 'Middle School 1'), ('MDS2', 'Middle School 2'), ('MDS3', 'Middle School 3'), ('MDS4', 'Middle School 4'), ('SHS1', 'High School 1'), ('SHS2', 'High School 2'), ('SHS3', 'High School 3'), ('SHS4', 'High School 4'), ('COL1', 'College Level 1'), ('COL2', 'College Level 2'), ('COL3', 'College Level 3'), ('COL4', 'College Level 4'), ('COL5', 'College Level 5'), ('LAW1', 'Law 1'), ('LAW2', 'Law 2'), ('LAW3', 'Law 3'), ('LAW4', 'Law 4'), ('MST1', 'Masters 1'), ('MST2', 'Masters 2'), ('MST3', 'Masters 3'), ('PHD1', 'Doctorate 1'), ('PHD2', 'Doctorate 2'), ('PHD3', 'Doctorate 3'), ('PHD4', 'Doctorate 4'), ('PHD5', 'Doctorate 5'), ('PHD6', 'Doctorate 6'), ('PHD7', 'Doctorate 7')], max_length=4)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='edu_admin.course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=255, unique=True)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='depts_created', to='register.employeedetail')),
                ('dept_head', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='dept_headed', to='register.employeedetail')),
                ('dept_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='edu_admin.department')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='depts_updated', to='register.employeedetail')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='dept_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='edu_admin.department'),
        ),
        migrations.CreateModel(
            name='ClassSubject',
            fields=[
                ('class_id', models.IntegerField(primary_key=True, serialize=False)),
                ('subject_block', models.CharField(max_length=10, unique=True)),
                ('semester', models.IntegerField(choices=[(1, '1st Semester'), (2, '2nd Semester'), (3, '3rd Semester')])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('active_flag', models.BooleanField(default=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.employeedetail')),
                ('subject_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='edu_admin.subject')),
            ],
        ),
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('schedule_id', models.IntegerField(primary_key=True, serialize=False)),
                ('day_of_wk', models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('active_flag', models.BooleanField(default=True)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='edu_admin.classsubject')),
            ],
        ),
    ]
