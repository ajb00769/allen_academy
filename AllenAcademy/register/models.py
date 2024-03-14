from django.db import models
from .custom import phone_validator
from .constants import (
    REGISTRATION_KEY_TYPES,
    SUFFIX_CHOICES,
    STUDENT_ACCOUNT_STATUS_CHOICES,
    SCHOLAR_TYPE_CHOICES,
    EMPLOYEE_ACCOUNT_STATUS_CHOICES,
    EMPLOYEE_TYPE_CHOICES,
    FAMILY_TYPE_CHOICES,
)


class RegistrationKey(models.Model):
    """
    A registration key is generated so that only verified users can
    create accounts. This is done to prevent random sign-ups to the
    internal school management system.

    generated_for follows: Last Name First Name Middle Name Suffix.
    Error will be raised if a registration key is used to register
    an account for someone with a different name.
    """

    generated_key = models.CharField(max_length=19, unique=True, null=False)
    key_type = models.CharField(
        max_length=3,
        choices=REGISTRATION_KEY_TYPES,
        null=False,
    )
    generated_for = models.CharField(max_length=255, null=False)
    key_expiry = models.DateField(null=False)
    key_used = models.BooleanField(default=False, null=False)


class AllAccountId(models.Model):
    """
    All ids generated from account creation are stored here to prevent
    account number collision.
    """

    generated_id = models.CharField(unique=True, null=False, max_length=9)


class StudentAccount(models.Model):
    student_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        null=False,
        on_delete=models.PROTECT,
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)
    allow_login = models.BooleanField(default=True, null=False)


class StudentDetail(models.Model):
    student_id = models.OneToOneField(
        "StudentAccount",
        to_field="student_id",
        null=False,
        on_delete=models.PROTECT,
    )
    first_name = models.CharField(null=False, max_length=80)
    middle_name = models.CharField(null=True, max_length=80)
    last_name = models.CharField(null=False, max_length=80)
    suffix = models.CharField(null=True, max_length=3, choices=SUFFIX_CHOICES)
    birthday = models.DateField(null=False)
    address = models.CharField(null=False, max_length=255)
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        null=True,
    )
    status = models.CharField(
        max_length=1,
        choices=STUDENT_ACCOUNT_STATUS_CHOICES,
        null=False,
    )
    scholar_type = models.CharField(
        max_length=1,
        choices=SCHOLAR_TYPE_CHOICES,
        null=False,
    )
    violations = models.BooleanField(default=False)


class EmployeeAccount(models.Model):
    employee_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        null=False,
        on_delete=models.PROTECT,
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)
    allow_login = models.BooleanField(default=True, null=False)


class EmployeeDetail(models.Model):
    employee_id = models.OneToOneField(
        "EmployeeAccount",
        to_field="employee_id",
        null=False,
        on_delete=models.PROTECT,
    )
    first_name = models.CharField(null=False, max_length=80)
    middle_name = models.CharField(null=True, max_length=80)
    last_name = models.CharField(null=False, max_length=80)
    suffix = models.CharField(null=True, max_length=3, choices=SUFFIX_CHOICES)
    birthday = models.DateField(null=False)
    address = models.CharField(null=False, max_length=255)
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        null=False,
    )
    employment_type = models.CharField(
        max_length=1,
        choices=EMPLOYEE_TYPE_CHOICES,
        null=False,
    )
    status = models.CharField(
        max_length=1,
        choices=EMPLOYEE_ACCOUNT_STATUS_CHOICES,
        null=False,
    )


class ParentAccount(models.Model):
    parent_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        null=False,
        on_delete=models.PROTECT,
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)
    allow_login = models.BooleanField(default=True, null=False)


class ParentDetail(models.Model):
    parent_id = models.OneToOneField(
        "ParentAccount",
        to_field="parent_id",
        on_delete=models.PROTECT,
    )
    first_name = models.CharField(null=False, max_length=80)
    middle_name = models.CharField(null=True, max_length=80)
    last_name = models.CharField(null=False, max_length=80)
    suffix = models.CharField(null=True, max_length=3, choices=SUFFIX_CHOICES)
    birthday = models.DateField(null=False)
    address = models.CharField(null=False, max_length=255)
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        null=False,
    )
    relationship = models.CharField(
        max_length=1,
        choices=FAMILY_TYPE_CHOICES,
        null=False,
    )
    student = models.ForeignKey(
        "StudentDetail",
        to_field="student_id",
        null=False,
        on_delete=models.CASCADE,
    )
