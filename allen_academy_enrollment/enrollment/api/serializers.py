from enrollment.models import StudentCourse, StudentSubjectBlock, EmployeeSubjectBlock
from rest_framework import serializers


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = "__all__"


class StudentSubjectBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectBlock
        fields = "__all__"


class EmployeeSubjectBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSubjectBlock
        fields = "__all__"
