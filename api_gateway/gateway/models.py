from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from gateway.model_utils.validators import (
    phone_validator,
    student_age_validator,
    staff_parent_age_validator,
)
from gateway.model_utils.choices import (
    REGISTRATION_KEY_TYPES,
    SUFFIX_CHOICES,
    STUDENT_ACCOUNT_STATUS_CHOICES,
    EMPLOYEE_ACCOUNT_STATUS_CHOICES,
    EMPLOYEE_TYPE_CHOICES,
    FAMILY_TYPE_CHOICES,
)
from gateway.model_utils.year_utils import (
    get_current_year,
    get_year_choices,
    get_current_date,
)

"""
Keyword Arguments Order:
-------------------------
1.  "Column Name"(for OneToOneField)
2.  to_field (for OneToOneField)
3.  primary_key
4.  on_delete (for ForeignKey, OneToOneField)
5.  choices
6.  validators
7.  max_length (for CharField and similar)
8.  db_index
9.  default
10. unique
11. blank
12. null
13. verbose_name
14. related_name (for ForeignKey, OneToOneField, ManyToManyField)
15. help_text

If a column has more than 2 keyword arguments opt for vertical arrangement
This is implemented to help with readability.
"""


class RegistrationKey(models.Model):
    """
    A registration key is generated so that only verified users can
    create accounts. This is done to prevent random sign-ups to the
    internal school management system.

    generated_for follows: Last Name First Name Middle Name Suffix.
    Error will be raised if a registration key is used to register
    an account for someone with a different name.
    """

    generated_key = models.CharField(
        primary_key=True,
        max_length=19,
        unique=True,
        null=False,
    )
    key_type = models.CharField(
        choices=REGISTRATION_KEY_TYPES,
        max_length=3,
        blank=False,
        null=False,
    )
    generated_for = models.CharField(
        max_length=255,
        db_index=False,
        blank=False,
        null=False,
    )
    key_expiry = models.DateField(null=False)
    key_used = models.BooleanField(
        db_index=False,
        default=False,
        null=False,
    )


class AllAccountId(models.Model):
    """
    All ids generated from account creation are stored here to prevent
    account number collision.
    """

    generated_id = models.CharField(primary_key=True, max_length=9)


class StudentAccount(models.Model):
    account_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        on_delete=models.PROTECT,
        primary_key=True,
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.BinaryField(
        max_length=255,
        db_index=False,
        blank=False,
        null=False,
    )
    allow_login = models.BooleanField(
        db_index=False,
        default=True,
        null=False,
    )


class StudentDetail(models.Model):
    account_id = models.OneToOneField(
        "StudentAccount",
        to_field="account_id",
        primary_key=True,
        on_delete=models.PROTECT,
    )
    last_name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )
    middle_name = models.CharField(
        max_length=80,
        db_index=False,
        default=None,
        null=True,
    )
    suffix = models.CharField(
        choices=SUFFIX_CHOICES,
        db_index=False,
        max_length=3,
        null=True,
    )
    birthday = models.DateField(
        validators=[student_age_validator],
        blank=False,
        null=False,
    )
    address = models.CharField(
        max_length=255,
        db_index=False,
        blank=False,
        null=False,
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        db_index=False,
        null=True,
    )
    status = models.CharField(
        choices=STUDENT_ACCOUNT_STATUS_CHOICES,
        max_length=1,
        db_index=False,
        default=STUDENT_ACCOUNT_STATUS_CHOICES[0][0],
        null=False,
    )


class EmployeeAccount(models.Model):
    account_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        on_delete=models.PROTECT,
        primary_key=True,
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.BinaryField(
        max_length=255,
        db_index=False,
        blank=False,
        null=False,
    )
    allow_login = models.BooleanField(
        db_index=False,
        default=True,
        null=False,
    )


class EmployeeDetail(models.Model):
    account_id = models.OneToOneField(
        "EmployeeAccount",
        to_field="account_id",
        primary_key=True,
        on_delete=models.PROTECT,
    )
    first_name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )
    middle_name = models.CharField(
        max_length=80,
        default=None,
        null=True,
    )
    last_name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )
    suffix = models.CharField(
        choices=SUFFIX_CHOICES,
        max_length=3,
        null=True,
    )
    birthday = models.DateField(
        validators=[staff_parent_age_validator],
        blank=False,
        null=False,
    )
    address = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        blank=False,
        null=False,
    )
    employment_type = models.CharField(
        choices=EMPLOYEE_TYPE_CHOICES,
        max_length=1,
        blank=False,
        null=False,
    )
    status = models.CharField(
        choices=EMPLOYEE_ACCOUNT_STATUS_CHOICES,
        max_length=1,
        default=EMPLOYEE_ACCOUNT_STATUS_CHOICES[0][0],
        null=False,
    )


class ParentAccount(models.Model):
    account_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        primary_key=True,
        on_delete=models.PROTECT,
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.BinaryField(
        max_length=255,
        blank=False,
        null=False,
    )
    allow_login = models.BooleanField(default=True, null=False)


class ParentDetail(models.Model):
    account_id = models.OneToOneField(
        "ParentAccount",
        to_field="account_id",
        primary_key=True,
        on_delete=models.PROTECT,
    )
    first_name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )
    middle_name = models.CharField(
        max_length=80,
        default=None,
        null=True,
    )
    last_name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )
    suffix = models.CharField(
        choices=SUFFIX_CHOICES,
        max_length=3,
        null=True,
    )
    birthday = models.DateField(
        validators=[staff_parent_age_validator],
        blank=False,
        null=False,
    )
    address = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        blank=False,
        null=False,
    )
    relationship = models.CharField(
        choices=FAMILY_TYPE_CHOICES,
        max_length=1,
        blank=False,
        null=False,
    )
    student = models.ForeignKey(
        "StudentDetail",
        to_field="account_id",
        on_delete=models.PROTECT,
        db_index=True,
        blank=False,
        null=False,
    )


# class Department(models.Model):
#     dept_id = models.CharField(
#         primary_key=True,
#         max_length=3,
#         blank=False,
#         null=False,
#     )
#     dept_parent = models.ForeignKey(
#         "self",
#         to_field="dept_id",
#         on_delete=models.PROTECT,
#         db_index=True,
#         blank=True,
#         null=True,
#     )
#     dept_name = models.CharField(
#         max_length=120,
#         blank=False,
#         null=False,
#     )
#     dept_head = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )


# class Salary(models.Model):
#     employee_id = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         primary_key=True,
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     salary = models.FloatField(blank=False, null=False)
#     created_by = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         primary_key=True,
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     create_date = models.DateField(auto_now_add=True)
#     changed_by = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     change_date = models.DateField()


# class EmployeeAttendance(models.Model):
#     employee_id = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         primary_key=True,
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     date_time_in = models.DateTimeField()
#     date_time_out = models.DateTimeField()


# class EmployeeSalaryHist(models.Model):
#     employee_id = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         primary_key=True,
#         on_delete=models.PROTECT,
#     )
#     salary_paid = models.FloatField(blank=False, null=False)
#     date_paid = models.DateField()
#     promotion_flag = models.BooleanField(max_length=1, default=False)
#     increase_flag = models.BooleanField(max_length=1, default=False)


# class StudentViolation(models.Model):
#     student_id = models.ForeignKey(
#         "StudentDetail",
#         to_field="account_id",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     violation_code = models.ForeignKey(
#         "ViolationCode",
#         to_field="violation_code",
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )


# class ViolationCode(models.Model):
#     violation_code = models.CharField(
#         primary_key=True,
#         max_length=3,
#         blank=False,
#         null=False,
#     )
#     violation_desc = models.CharField(
#         max_length=1024,
#         blank=False,
#         null=False,
#     )


# class Course(models.Model):
#     course_code = models.CharField(
#         primary_key=True,
#         max_length=10,
#         blank=False,
#         null=False,
#     )
#     course_name = models.CharField(
#         max_length=255,
#         blank=False,
#         null=False,
#     )
#     total_units = models.IntegerField()
#     dept_id = models.ForeignKey(
#         "Department",
#         to_field="dept_id",
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )


# class Subject(models.Model):
#     subject_code = models.CharField(
#         primary_key=True,
#         max_length=10,
#         blank=False,
#         null=False,
#     )
#     subject_type = models.CharField(
#         max_length=3,
#         blank=False,
#         null=False,
#     )
#     subject_name = models.CharField(
#         max_length=512,
#         blank=False,
#         null=False,
#     )
#     subject_units = models.IntegerField(blank=False, null=False)
#     weekly_hours = models.DurationField(blank=False, null=False)
#     subject_tuition = models.FloatField(blank=False, null=False)
#     dept_id = models.ForeignKey(
#         "Departments",
#         to_field="dept_id",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )


# class ClassSubject(models.Model):
#     class_id = models.IntegerField(primary_key=True)
#     subject_code = models.ForeignKey(
#         "Subject",
#         to_field="subject_code",
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )
#     subj_block = models.CharField(
#         max_length=10,
#         blank=False,
#         null=False,
#     )
#     professor = models.ForeignKey(
#         "EmployeeDetail",
#         to_field="account_id",
#         on_delete=models.CASCADE,
#         null=False,
#     )
#     semester = models.IntegerField(
#         choices=[1, 2],
#         blank=False,
#         null=False,
#     )
#     school_year = models.IntegerField(
#         choices=get_year_choices(),
#         default=get_current_year(),
#         null=False,
#     )
#     start_date = models.DateField(blank=False, null=False)
#     end_date = models.DateField(blank=False, null=False)
#     completed = models.BooleanField(default=False)
#     active_flag = models.BooleanField(default=True)

#     def clean(self):
#         super().clean()
#         if self.start_date >= self.end_date:
#             raise ValidationError("End date should be higher than the start date.")
#         if self.end_date >= get_current_date():
#             raise ValidationError("End date should be higher than the current date.")

#     # TODO: Create a scheduled job to run once a day to check the if end_date >= current_date to change the flag


# class ClassSchedule(models.Model):
#     """
#     Multiple rows for similar classes but different schedules.
#     """

#     schedule_id = models.IntegerField(primary_key=True)
#     class_id = models.ForeignKey(
#         "ClassSubject",
#         to_field="class_id",
#         on_delete=models.CASCADE,
#         null=False,
#     )
#     day_of_week = models.IntegerField(choices=[i for i in range(7)])
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     purge_flag = models.BooleanField(default=False)


# class StudentSubject(models.Model):
#     student_id = models.ForeignKey(
#         "StudentDetail",
#         to_field="account_id",
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )
#     subject_code = models.ForeignKey(
#         "Subject",
#         to_field="subject_code",
#         on_delete=models.CASCADE,
#     )
#     year = models.IntegerField(
#         choices=get_year_choices(),
#         default=get_current_year(),
#         null=False,
#     )
#     status = models.CharField(max_length=1)  # pass fail or active


# class StudentSchedule(models.Model):
#     student_id = models.ForeignKey(
#         "StudentSubject",
#         to_field="student_id",
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )
#     schedule_id = models.ForeignKey(
#         "ClassSchedule",
#         to_field="schedule_id",
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )


# class Grade(models.Model):
#     student_id = models.ForeignKey(
#         "StudentSubject",
#         to_field="student_id",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     subject_id = models.ForeignKey(
#         "StudentSubject",
#         to_field="subject_code",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     class_id = models.ForeignKey(
#         "StudentSubject",
#         to_field="student_id",
#         on_delete=models.PROTECT,
#         blank=False,
#         null=False,
#     )
#     grade = models.FloatField()
