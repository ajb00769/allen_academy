from rest_framework import serializers
from register.models import (
    AllAccountIds,
    EmployeeAccounts,
    StudentAccounts,
    ParentAccounts,
)


class AccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllAccountIds
        fields = "__all__"
