from rest_framework import serializers
from edu_admin.models import (
    Department,
    Course,
    CourseSubject,
    SubjectBlock,
    ClassSchedule,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubject
        fields = "__all__"


class SubjectBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectBlock
        fields = "__all__"


class ClassScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = "__all__"
