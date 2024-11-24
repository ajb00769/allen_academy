import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime
from custom_common.jwt_handler import handle_jwt
from register.models import EmployeeDetail
from edu_admin.models import Department
from edu_admin.api.serializers import (
    DepartmentSerializer,
    CourseSerializer,
    CourseSubjectSerializer,
    SubjectBlockSerializer,
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

    jwt_decode = jwt.decode(
        request.data.get("token"), settings.JWT_SECRET_KEY, algorithms=["HS256"]
    )
    user_id = jwt_decode.get("user_id")

    clean_input = request.data.copy()
    clean_input.pop("created_on", None)
    clean_input.pop("updated_on", None)
    clean_input.update({"updated_on": datetime.now()})

    try:
        existing = Department.objects.get(dept_id=clean_input.get("dept_id"))
        existing.dept_id = clean_input.get("dept_id")
        existing.dept_parent = clean_input.get("dept_parent")
        existing.dept_name = clean_input.get("dept_name")

        try:
            existing.dept_head = EmployeeDetail.objects.get(
                account_id=clean_input.get("dept_head")
            )
            existing.updated_by = EmployeeDetail.objects.get(account_id=user_id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "employee_invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        except MultipleObjectsReturned:
            return Response(
                {"error": "data_integrity_error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        """
        # BUGFIX: 94e6oWUB - FIXED
        Bug was found here, data was not saving because of the missing () in .save
        Also fixed a warning about a non-timezone-aware datetime object being passed
        into the db. Using django.utils.timezone instead of datetime.datetime
        """
        existing.updated_on = timezone.now()
        existing.save()

        existing_serializer = DepartmentSerializer(existing)
        return Response(existing_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        clean_input.update({"created_on": datetime.now()})
        clean_input.pop("updated_on", None)
        department_serializer = DepartmentSerializer(data=clean_input)

        with transaction.atomic():
            if department_serializer.is_valid():
                department_serializer.save()
                return Response(
                    department_serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {"error": department_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except MultipleObjectsReturned:
        return Response(
            {"error": "data_integrity_error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

    subject_serializer = CourseSubjectSerializer(data=request.data)

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

    class_subject_serializer = SubjectBlockSerializer(data=request.data)

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
