from django.db import models


class AllAccountIds(models.Model):
    """
    All ids generated from account creation are stored here
    to prevent account number collision.
    """

    generated_id = models.IntegerField(unique=True, null=False)


class StudentAccounts(models.Model):
    student_id = models.ForeignKey(
        "AllAccountIds", to_field="generated_id", on_delete=models.CASCADE
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)


class EmployeeAccounts(models.Model):
    employee_id = models.ForeignKey(
        "AllAccountIds", to_field="generated_id", on_delete=models.CASCADE
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)


class ParentAccounts(models.Model):
    parent_id = models.ForeignKey(
        "AllAccountIds", to_field="generated_id", on_delete=models.CASCADE
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)
