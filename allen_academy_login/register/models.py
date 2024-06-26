from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from register.custom_utils.custom import (
    phone_validator,
    student_age_validator,
    staff_parent_age_validator,
)
from register.custom_utils.constants import (
    REGISTRATION_KEY_TYPES,
    SUFFIX_CHOICES,
    STUDENT_ACCOUNT_STATUS_CHOICES,
    SCHOLAR_TYPE_CHOICES,
    EMPLOYEE_ACCOUNT_STATUS_CHOICES,
    EMPLOYEE_TYPE_CHOICES,
    FAMILY_TYPE_CHOICES,
    ELEMENTARY_SCHOOL_CHOICES,
    MIDDLE_SCHOOL_CHOICES,
    HIGH_SCHOOL_CHOICES,
    COLLEGE_LEVEL_CHOICES,
    LAW_CHOICES,
    MASTERS_CHOICES,
    PHD_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES,
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
        blank=False,
        null=False,
    )
    year_level = models.CharField(
        choices=[
            *ELEMENTARY_SCHOOL_CHOICES,
            *MIDDLE_SCHOOL_CHOICES,
            *HIGH_SCHOOL_CHOICES,
            *COLLEGE_LEVEL_CHOICES,
            *LAW_CHOICES,
            *MASTERS_CHOICES,
            *PHD_CHOICES,
            *EMPLOYEE_YEAR_LEVEL_CHOICES,
        ],
        blank=False,
        null=False,
    )
    key_expiry = models.DateField(null=False)
    key_used = models.BooleanField(default=False, null=False)


class AllAccountId(models.Model):
    """
    All ids generated from account creation are stored here to prevent
    account number collision.
    """

    generated_id = models.CharField(primary_key=True, max_length=9)


class AllAccount(AbstractUser):
    account_id = models.OneToOneField(
        "AllAccountId",
        to_field="generated_id",
        on_delete=models.PROTECT,
        primary_key=True,
    )
    account_type = models.CharField(
        choices=REGISTRATION_KEY_TYPES,
        max_length=3,
        db_index=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=150,
        db_index=True,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    groups = models.ManyToManyField(
        Group,
        related_name="common_user_groups",
        blank=True,
        help_text="The groups this user belongs to. Users are granted permissions relative to the groups they belong to",
        verbose_name="common user groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="common_user_permissions",
        blank=True,
        help_text="Specific user permissions.",
        verbose_name="common user permissions",
    )


class StudentDetail(models.Model):
    account_id = models.OneToOneField(
        "AllAccount",
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
        default=None,
        null=True,
    )
    suffix = models.CharField(
        choices=SUFFIX_CHOICES,
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
        blank=False,
        null=False,
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        null=True,
    )
    status = models.CharField(
        choices=STUDENT_ACCOUNT_STATUS_CHOICES,
        max_length=1,
        default=STUDENT_ACCOUNT_STATUS_CHOICES[0][0],
        null=False,
    )
    current_yr_lvl = models.CharField(
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
    scholarship_type = models.CharField(
        choices=SCHOLAR_TYPE_CHOICES,
        max_length=1,
        default=SCHOLAR_TYPE_CHOICES[0][0],
        blank=True,
    )

    def is_elementary(self) -> bool:
        return self.current_yr_lvl in dict(ELEMENTARY_SCHOOL_CHOICES)

    def is_middle_school(self) -> bool:
        return self.current_yr_lvl in dict(MIDDLE_SCHOOL_CHOICES)

    def is_high_school(self) -> bool:
        return self.current_yr_lvl in dict(HIGH_SCHOOL_CHOICES)

    def is_college(self) -> bool:
        return self.current_yr_lvl in dict(COLLEGE_LEVEL_CHOICES)

    def is_law(self) -> bool:
        return self.current_yr_lvl in dict(LAW_CHOICES)

    def is_masters(self) -> bool:
        return self.current_yr_lvl in dict(MASTERS_CHOICES)

    def is_phd(self) -> bool:
        return self.current_yr_lvl in dict(PHD_CHOICES)


class EmployeeDetail(models.Model):
    account_id = models.OneToOneField(
        "AllAccount",
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
    teaching_year_lvl = models.CharField(
        choices=EMPLOYEE_YEAR_LEVEL_CHOICES,
        max_length=16,
        default=EMPLOYEE_YEAR_LEVEL_CHOICES[0][0],
        blank=False,
    )

    def is_dean(self) -> bool:
        return self.employment_type == "D"

    def is_teacher(self) -> bool:
        return self.employment_type == "T"

    def is_admin_staff(self) -> bool:
        return self.employment_type == "A"


class ParentDetail(models.Model):
    account_id = models.OneToOneField(
        "AllAccount",
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
