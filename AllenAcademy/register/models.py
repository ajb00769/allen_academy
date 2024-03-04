from django.db import models


class AllAccountIds(models.Model):
    """
    All ids generated from account creation are stored here
    to ensure no account numbers are unique to each user.
    """

    generated_id = models.IntegerField(unique=True, null=False)


class StudentAccounts(models.Model):
    student_id = models.ForeignKey(AllAccountIds.generated_id, on_delete=models.CASCADE)
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)


class EmployeeAccounts(models.Model):
    employee_id = models.ForeignKey(
        AllAccountIds.generated_id, on_delete=models.CASCADE
    )
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)


class ParentAccounts(models.Model):
    parent_id = models.ForeignKey(AllAccountIds.generated_id, on_delete=models.CASCADE)
    email = models.EmailField(null=False)
    password = models.BinaryField(max_length=255, null=False)
