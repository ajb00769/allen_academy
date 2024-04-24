from django.db import models

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
        blank=False,
        null=False,
    )
    allow_login = models.BooleanField(default=True, null=False)


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
        blank=False,
        null=False,
    )
    allow_login = models.BooleanField(default=True, null=False)


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
