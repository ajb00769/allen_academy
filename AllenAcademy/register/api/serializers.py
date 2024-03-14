from rest_framework import serializers
from register.models import (
    RegistrationKey,
    AllAccountId,
    StudentAccount,
    StudentDetail,
    EmployeeAccount,
    EmployeeDetail,
    ParentAccount,
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


class StudentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAccount
        fields = "__all__"


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = "__all__"


class EmployeeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAccount
        fields = "__all__"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDetail
        fields = "__all__"


class ParentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentAccount
        fields = "__all__"


class ParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentDetail
        fields = "__all__"
