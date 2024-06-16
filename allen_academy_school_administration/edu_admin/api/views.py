from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from custom_common.jwt_handler import handle_jwt
from edu_admin.api.serializers import (
    DepartmentSerializer,
    CourseSerializer,
    SubjectSerializer,
    ClassSubjectSerializer,
    ClassScheduleSerializer,
)
from edu_admin.custom_utils.custom import (
    class_end_date_validator,
    class_end_time_validator,
)


@api_view(["POST"])
def create_department(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)

    department_serializer = DepartmentSerializer(data=request.data)

    with transaction.atomic():
        if department_serializer.is_valid():
            department_serializer.save()
            return Response(department_serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": department_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def create_course(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)

    course_serializer = CourseSerializer(data=request.data)

    with transaction.atomic():
        if course_serializer.is_valid():
            course_serializer.save()
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": course_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def create_subject(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)

    subject_serializer = SubjectSerializer(data=request.data)

    with transaction.atomic():
        if subject_serializer.is_valid():
            subject_serializer.save()
            return Response(subject_serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": subject_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def create_subject_block(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)

    try:
        class_end_date_validator(
            request.data.get("start_date"), request.data.get("end_date")
        )
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_406_NOT_ACCEPTABLE)

    class_subject_serializer = ClassSubjectSerializer(data=request.data)

    with transaction.atomic():
        if class_subject_serializer.is_valid():
            class_subject_serializer.save()
            return Response(
                {"success": class_subject_serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": class_subject_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def create_schedule(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)

    try:
        class_end_time_validator(
            request.data.get("start_time"), request.data.get("end_time")
        )
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_406_NOT_ACCEPTABLE)

    schedule_serializer = ClassScheduleSerializer(data=request.data)

    with transaction.atomic():
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return Response(
                {"success": schedule_serializer.data}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": schedule_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
