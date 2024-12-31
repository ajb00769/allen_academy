import jwt
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
    SubjectBlockSerializer,
    ClassScheduleSerializer,
)
from enrollment.custom_utils.mapping import (
    teacher_student_yr_lvl_mapping,
    enrollment_mapping,
)
from enrollment.models import StudentCourse
from enrollment.api.serializers import StudentCourseSerializer
from register.models import AllAccount
from register.api.serializers import AllAccountSerializer


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
def get_subject_block(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    subject_code = request.data.get("subject_code")
    subject_blocks = SubjectBlockSerializer(
        SubjectBlock.objects.filter(subject_code=subject_code), many=True
    ).data
    return Response({"result": subject_blocks}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_block_schedule(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    block_id = request.data.get("block_id")
    schedules = ClassScheduleSerializer(
        ClassSchedule.objects.filter(block_id=block_id), many=True
    ).data
    return Response({"result": schedules}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_subject_schedule_list(request):
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
def get_course(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    account_id = result.get("user_id")

    try:
        account_data = AllAccountSerializer(
            AllAccount.objects.get(account_id=account_id)
        ).data
        account_type = account_data.get("account_type")

        if account_type == "STU":
            student_course_data = StudentCourseSerializer(
                StudentCourse.objects.get(student_id=account_id)
            ).data
            enrolled_course = student_course_data.get("course_id")

            course_data = CourseSerializer(
                Course.objects.get(course_code=enrolled_course)
            ).data
            course_code = course_data.get("course_code")
            course_name = course_data.get("course_name")
            course_dept_id = course_data.get("dept_id")

            department_data = DepartmentSerializer(
                Department.objects.get(dept_id=course_dept_id)
            ).data
            department_name = department_data.get("dept_name")

        elif account_type == "EMP":
            return Response({"account_type": account_type}, status=status.HTTP_200_OK)

    except MultipleObjectsReturned:
        return Response(
            {"error": "data_integrity_issue"}, status=status.HTTP_409_CONFLICT
        )
    except ObjectDoesNotExist:
        return Response(
            {"warning": "not_enrolled_to_course"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
    return Response(
        {
            "course_code": course_code,
            "course": course_name,
            "college": department_name,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def enroll_course(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    """
    # BUGFIX: 1TABeLzU - FIXED
    Problematic piece of code was found here. It was checking the JWT for the account_id
    to be registered/enrolled when it should have just been checking the account_id in 
    the normal payload instead. That's why it was returning invvalid account type because
    the logic below only allows account_type "STU" to be enrolled, in the JWT the account
    is of type "EMP" which is being passed.

    Correct logic now reflects where only "EMP" can enroll users of type "STU" to a course.
    """
    if not StudentDetail.objects.get(account_id=request.data.get("account_id")):
        return Response(
            {"error": "unauthorized_account_type"}, status=status.HTTP_401_UNAUTHORIZED
        )

    student_id = request.data.get("account_id")
    course_code = request.data.get("course_code")

    try:
        has_course = StudentCourse.objects.get(student_id=student_id)
        if has_course:
            return Response(
                {"error": "already_enrolled_to_a_course"},
                status=status.HTTP_409_CONFLICT,
            )
    except ObjectDoesNotExist:
        pass

    """
    # BUGFIX: 1TABeLzU - FIXED
    Another problematic piece of code was also found here where the wrong key "course_code"
    was being passed into the StudentCourse table which only has "course_id" hence returning
    and error of "unable_to_enroll_course".

    It was also previously attempting to store it in a different table "StudentSubjectBlock"
    which was not what was intended. Replaced wtih the correct table "StudentCourse".
    """
    payload = {"student_id": student_id, "course_id": course_code}
    serializer = StudentCourseSerializer(data=payload)

    with transaction.atomic():
        if serializer.is_valid():
            serializer.save()
            return Response({"success": serializer.data}, status=status.HTTP_200_OK)

    return Response(
        {"error": "unable_to_enroll_course"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
def enroll_subject_schedule(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded = jwt.decode(
            request.data.get("token"), settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    except Exception:
        return Response(
            {"error": "unable_to_decode_jwt"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    account_id = decoded.get("user_id")
    account_type = decoded.get("account_type")
    block_id = request.data.get("block_id")

    if account_type == "PAR":
        return Response(
            {"error": "invalid_account_type"}, status=status.HTTP_403_FORBIDDEN
        )

    try:
        if any(var is None for var in [account_id, account_type, block_id]):
            raise Exception("required_field_is_null")

        schedules = [
            schedule.schedule_id
            for schedule in ClassSchedule.objects.filter(block_id=block_id)
        ]

        subject_code = SubjectBlockSerializer(
            SubjectBlock.objects.select_related("subject_code")
            .filter(block_id=block_id)
            .first()
        ).data.get("subject_code")

        subject_course = CourseSubjectSerializer(
            CourseSubject.objects.get(subject_code=subject_code)
        ).data.get("course_code")

        student_course = StudentCourseSerializer(
            StudentCourse.objects.get(student_id=account_id)
        ).data.get("course_id")

        if subject_course != student_course:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        if account_type == "STU":
            return Response(
                {"error": "not_enrolled_to_course_of_subject"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for schedule_id in schedules:
        proposed_schedule = ClassSchedule.objects.get(schedule_id=schedule_id)
        # get the data model for user-block/schedule to return results of all enrolled schedules
        enrollment_model = enrollment_mapping.get(account_type).get("model")
        existing_schedule_obj = enrollment_model.objects.filter(account_id=account_id)
        existing_schedule_arr = [
            schedule.get_schedule_details()
            for schedule in existing_schedule_obj
            if schedule.get_schedule_details().day_of_wk == proposed_schedule.day_of_wk
            and (
                proposed_schedule.start_time < schedule.get_schedule_details().end_time
                or proposed_schedule.end_time
                < schedule.get_schedule_details().start_time
            )
        ]
        # print(f"***\n\n\n\nDEBUG ATTENTION: {existing_schedule_arr}\n\n\n\n***")
        # an array of ClassSchedule objects that have the same day of week of the prospect schedule to add for the user

        if existing_schedule_arr:
            return Response(
                {"error": "schedule_conflict"}, status=status.HTTP_400_BAD_REQUEST
            )

    with transaction.atomic():
        for schedule_id in schedules:
            verified_payload = {"account_id": account_id, "schedule_id": schedule_id}
            enrollment_serializer = enrollment_mapping.get(account_type).get(
                "serializer"
            )
            serializer = enrollment_serializer(data=verified_payload)

            if serializer.is_valid():
                serializer.save()

        return Response({"success": serializer.data}, status=status.HTTP_200_OK)

    return Response(
        {"error": "unable_to_enroll_subject"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
def get_user_schedule(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded = jwt.decode(
            request.data.get("token"), settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    except Exception:
        return Response(
            {"error": "unable_to_decode_jwt"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    account_id = decoded.get("user_id")
    account_type = decoded.get("account_type")

    enrollment_model = enrollment_mapping.get(account_type).get("model")

    schedules = enrollment_model.objects.filter(account_id=account_id).select_related(
        "schedule_id__block_id__subject_code"
    )

    desired_keys = [
        "block_id",
        "semester",
        "start_date",
        "end_date",
        "subject_code",
        "day_of_wk",
        "room_no",
        "start_time",
        "end_time",
        "subject_type",
        "subject_name",
        "subject_units",
        "subject_tuition",
        "course_yr_lvl",
        "course_code",
        "first_name",
        "middle_name",
        "last_name",
        "suffix",
    ]

    raw_sched_list = [
        {
            **SubjectBlockSerializer(schedule.schedule_id.block_id).data,
            **ClassScheduleSerializer(schedule.schedule_id).data,
            **CourseSubjectSerializer(schedule.schedule_id.block_id.subject_code).data,
            **EmployeeDetailSerializer(schedule.schedule_id.block_id.professor).data,
        }
        for schedule in schedules
        if schedule.schedule_id.active_flag
    ]

    sched_list = [
        {k: v for k, v in item.items() if k in desired_keys} for item in raw_sched_list
    ]

    return Response({"result": sched_list}, status=status.HTTP_200_OK)
