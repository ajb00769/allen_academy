from django.db import models
from edu_admin.custom_utils.constants import (
    ELEMENTARY_SCHOOL_CHOICES,
    MIDDLE_SCHOOL_CHOICES,
    HIGH_SCHOOL_CHOICES,
    COLLEGE_LEVEL_CHOICES,
    LAW_CHOICES,
    MASTERS_CHOICES,
    PHD_CHOICES,
    SEMESTER_CHOICES,
    SUBJECT_TYPE_CHOICES,
    DAY_NAMES,
)


class Department(models.Model):
    dept_id = models.CharField(
        primary_key=True,
        max_length=10,
        blank=False,
        null=False,
    )
    dept_parent = models.ForeignKey(
        "Department",
        to_field="dept_id",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
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
        blank=True,
        null=True,
    )
    updated_on = models.DateTimeField(blank=True, null=True)


class Course(models.Model):
    course_code = models.CharField(
        primary_key=True,
        max_length=10,
        blank=False,
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


class CourseSubject(models.Model):
    subject_code = models.CharField(
        primary_key=True,
        max_length=10,
        blank=False,
        null=False,
    )
    subject_type = models.CharField(
        choices=SUBJECT_TYPE_CHOICES,
        blank=False,
        null=False,
    )
    subject_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    subject_units = models.IntegerField(blank=False, null=False)
    wk_class_dura = models.IntegerField(
        blank=False, null=False
    )  # INFO: expressed as number of hours per week
    subject_tuition = models.FloatField(blank=False, null=False)
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

    def is_elementary(self) -> bool:
        return self.course_yr_lvl in dict(ELEMENTARY_SCHOOL_CHOICES)

    def is_middle_school(self) -> bool:
        return self.course_yr_lvl in dict(MIDDLE_SCHOOL_CHOICES)

    def is_high_school(self) -> bool:
        return self.course_yr_lvl in dict(HIGH_SCHOOL_CHOICES)

    def is_college(self) -> bool:
        return self.course_yr_lvl in dict(COLLEGE_LEVEL_CHOICES)

    def is_law(self) -> bool:
        return self.course_yr_lvl in dict(LAW_CHOICES)

    def is_masters(self) -> bool:
        return self.course_yr_lvl in dict(MASTERS_CHOICES)

    def is_phd(self) -> bool:
        return self.course_yr_lvl in dict(PHD_CHOICES)


class SubjectBlock(models.Model):
    block_id = models.CharField(
        max_length=10,
        unique=True,
        blank=False,
        null=False,
    )
    subject_code = models.ForeignKey(
        "CourseSubject",
        to_field="subject_code",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    professor = models.ForeignKey(
        "register.EmployeeDetail",
        to_field="account_id",
        on_delete=models.PROTECT,
    )
    semester = models.IntegerField(
        choices=SEMESTER_CHOICES,
        blank=False,
        null=False,
    )
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    completed = models.BooleanField(default=False)
    active_flag = models.BooleanField(default=True)

    def is_active(self) -> bool:
        return self.active_flag

    def get_school_year(self) -> str:
        school_year_start = self.start_date.year
        school_year_end = school_year_start + 1
        return f"{school_year_start} - {school_year_end}"


class ClassSchedule(models.Model):
    schedule_id = models.IntegerField(
        primary_key=True,
        blank=False,
        null=False,
    )
    block_id = models.ForeignKey(
        "SubjectBlock",
        to_field="block_id",
        on_delete=models.PROTECT,
    )
    day_of_wk = models.CharField(
        choices=DAY_NAMES,
        blank=False,
        null=False,
    )
    room_no = models.CharField(
        max_length=10,
        default="TBA",
        blank=True,
    )
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    active_flag = models.BooleanField(default=True)
