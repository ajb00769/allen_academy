from rest_framework import serializers
from register.models import (
    RegistrationKey,
    AllAccountId,
    AllAccount,
    StudentDetail,
    EmployeeDetail,
    ParentDetail,
)


class RegistrationKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationKey
        fields = "__all__"


class AccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllAccountId
        fields = "__all__"


class AllAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllAccount
        fields = "__all__"


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = "__all__"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDetail
        fields = "__all__"


class ParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentDetail
        fields = "__all__"
