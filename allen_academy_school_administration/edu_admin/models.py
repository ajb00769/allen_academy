from django.db import models
from register.custom_utils.constants import (
    ELEMENTARY_SCHOOL_CHOICES,
    MIDDLE_SCHOOL_CHOICES,
    HIGH_SCHOOL_CHOICES,
    COLLEGE_LEVEL_CHOICES,
    LAW_CHOICES,
    MASTERS_CHOICES,
    PHD_CHOICES,
)


class Department(models.Model):
    dept_id = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True,
        null=False,
    )
    dept_parent = models.ForeignKey(
        "Department",
        to_field="dept_id",
        on_delete=models.PROTECT,
    )
    dept_name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
    )
    dept_head = models.OneToOneField(
        "register.EmployeeDetail",
        to_field="account_id",
        on_delete=models.PROTECT,
        null=False,
        related_name="dept_headed",
    )
    created_by = models.ForeignKey(
        "register.EmployeeDetail",
        to_field="account_id",
        on_delete=models.PROTECT,
        null=False,
        related_name="depts_created",
    )
    created_on = models.DateTimeField(null=False)
    updated_by = models.ForeignKey(
        "register.EmployeeDetail",
        to_field="account_id",
        on_delete=models.PROTECT,
        related_name="depts_updated",
    )
    updated_on = models.DateTimeField()


class Course(models.Model):
    course_code = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True,
        null=False,
    )
    course_name = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        blank=False,
        null=False,
    )
    total_units = models.IntegerField(blank=False, null=False)
    dept_id = models.ForeignKey(
        "Department",
        to_field="dept_id",
        on_delete=models.PROTECT,
        null=False,
    )


class Subject(models.Model):
    subject_code = models.CharField(primary_key=True, max_length=10)
    subject_type = models.CharField()
    subject_name = models.CharField(max_length=255)
    subject_units = models.IntegerField()
    wk_class_dura = models.IntegerField()
    subject_tuition = models.FloatField()
    course_code = models.ForeignKey(
        "Course",
        to_field="course_code",
        on_delete=models.PROTECT,
    )
    course_yr_lvl = models.CharField(
        max_length=4,
        choices=[
            *ELEMENTARY_SCHOOL_CHOICES,
            *MIDDLE_SCHOOL_CHOICES,
            *HIGH_SCHOOL_CHOICES,
            *COLLEGE_LEVEL_CHOICES,
            *LAW_CHOICES,
            *MASTERS_CHOICES,
            *PHD_CHOICES,
        ],
        blank=False,
        null=False,
    )

    def is_elementary(self):
        return self.course_yr_lvl in dict(ELEMENTARY_SCHOOL_CHOICES)

    def is_middle_school(self):
        return self.course_yr_lvl in dict(MIDDLE_SCHOOL_CHOICES)

    def is_high_school(self):
        return self.course_yr_lvl in dict(HIGH_SCHOOL_CHOICES)

    def is_college(self):
        return self.course_yr_lvl in dict(COLLEGE_LEVEL_CHOICES)

    def is_law(self):
        return self.course_yr_lvl in dict(LAW_CHOICES)

    def is_masters(self):
        return self.course_yr_lvl in dict(MASTERS_CHOICES)

    def is_phd(self):
        return self.course_yr_lvl in dict(PHD_CHOICES)


class ClassSubject(models.Model):
    class_id = models.IntegerField(primary_key=True)
    subject_code = models.ForeignKey(
        "Subject",
        to_field="subject_code",
        on_delete=models.PROTECT,
    )
    subject_block = models.CharField()
    professor = models.ForeignKey(
        "register.EmployeeDetail",
        to_field="account_id",
        on_delete=models.PROTECT,
    )
    semester = models.IntegerField()
    school_year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField()
    active_flag = models.BooleanField()

    def is_active(self):
        return self.active_flag


class ClassSchedule(models.Model):
    schedule_id = models.IntegerField(primary_key=True)
    class_id = models.ForeignKey(
        "ClassSubject",
        to_field="class_id",
        on_delete=models.PROTECT,
    )
    day_of_wk = models.CharField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    active_flag = models.BooleanField()
