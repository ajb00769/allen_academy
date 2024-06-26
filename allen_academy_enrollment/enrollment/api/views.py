import jwt
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from custom_common.jwt_handler import handle_jwt
from register.models import EmployeeDetail, StudentDetail
from register.api.serializers import EmployeeDetailSerializer, StudentDetailSerializer
from edu_admin.models import (
    Department,
    Course,
    CourseSubject,
    SubjectBlock,
    ClassSchedule,
)
from edu_admin.api.serializers import (
    DepartmentSerializer,
    CourseSerializer,
    CourseSubjectSerializer,
    ClassScheduleSerializer,
)
from enrollment.custom_utils.mapping import (
    teacher_student_yr_lvl_mapping,
    enrollment_mapping,
)


@api_view(["GET"])
def get_dept_list(request):
    try:
        depts = DepartmentSerializer(Department.objects.all(), many=True).data
        dept_names = [
            {dept_name.get("dept_id"): dept_name.get("dept_name")}
            for dept_name in depts
        ]
        return Response({"departments": dept_names}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "get_dept_list_exception"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_course_list(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    dept_id = request.data.get("dept_id")
    if dept_id is None:
        return Response(
            {"error": "no_dept_id_supplied"}, status=status.HTTP_400_BAD_REQUEST
        )

    courses = CourseSerializer(Course.objects.filter(dept_id=dept_id), many=True).data
    courses_list = [
        {course.get("course_code"): course.get("course_name")} for course in courses
    ]
    return Response({"courses": courses_list}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_subject_list(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    course_id = request.data.get("course_id")
    if course_id is None:
        return Response(
            {"error": "no_course_id_supplied"}, status=status.HTTP_400_BAD_REQUEST
        )

    payload = jwt.decode(
        request.data.get("token"), settings.JWT_SECRET_KEY, algorithms=["HS256"]
    )

    account_type = payload.get("account_type")
    account_id = str(payload.get("user_id"))

    if account_type == "PAR":
        return Response(
            {"error": "unauthorized_account_type"}, status=status.HTTP_401_UNAUTHORIZED
        )
    elif account_type == "EMP":
        teaching_year_lvl = EmployeeDetailSerializer(
            EmployeeDetail.objects.get(account_id=account_id)
        ).data.get("teaching_year_lvl")

        subject_mapping = [
            dict_item[0]
            for dict_item in teacher_student_yr_lvl_mapping.get(teaching_year_lvl)
        ]

        subjects = CourseSubjectSerializer(
            CourseSubject.objects.filter(
                course_code=course_id, course_yr_lvl__in=subject_mapping
            ),
            many=True,
        ).data
        return Response({"result": subjects}, status=status.HTTP_200_OK)
    elif account_type == "STU":
        student_obj = StudentDetailSerializer(
            StudentDetail.objects.get(account_id=account_id)
        )
        student_yr_lvl = student_obj.data.get("current_yr_lvl")
        subjects = CourseSubjectSerializer(
            CourseSubject.objects.filter(
                course_code=course_id, course_yr_lvl=student_yr_lvl
            ),
            many=True,
        ).data
        return Response({"result": subjects}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_subject_schedules(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    subject_code = request.data.get("subject_code")
    subject_blocks = SubjectBlock.objects.filter(subject_code=subject_code)
    block_ids = [block.block_id for block in subject_blocks]
    block_schedules = ClassScheduleSerializer(
        ClassSchedule.objects.filter(block_id__in=block_ids),
        many=True,
    ).data
    return Response({"result": block_schedules}, status=status.HTTP_200_OK)


@api_view(["POST"])
def enroll_course(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    pass  # enroll into the selected subject-block-schedule


@api_view(["POST"])
def enroll_subjects(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded = jwt.decode(
            request.data.get("token"), settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        account_id = decoded.get("user_id")
        account_type = decoded.get("account_type")
        schedule_id = request.data.get("schedule_id")

        if any(var is None for var in [account_id, account_type, schedule_id]):
            raise Exception("required_field_is_null")

        payload = {"account_id": account_id, "schedule_id": schedule_id}

        enrollment_serializer = enrollment_mapping[account_type]["serializer"]
        serializer = enrollment_serializer(data=payload)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}, status=status.HTTP_200_OK)
        return Response(
            {"error": "unable_to_enroll"}, status=status.HTTP_400_BAD_REQUEST
        )

        with transaction.atomic():
            pass
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_enrolled_subjects(request):
    pass
