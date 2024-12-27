import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from login.api.serializers import CustomTokenObtainPairSerializer
from register.models import AllAccount, EmployeeDetail, ParentDetail, StudentDetail
from register.api.serializers import (
    EmployeeDetailSerializer,
    ParentDetailSerializer,
    StudentDetailSerializer,
)


@api_view(["POST"])
def login(request):
    token = request.data.get("token")
    if token is not None:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        try:
            user_obj = AllAccount.objects.get(account_id=decoded.get("user_id"))
            if not user_obj.is_active:
                return Response(
                    {"error": "cannot_give_token_to_banned_user"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            refresh = RefreshToken.for_user(user_obj)
            refresh.payload["user_id"] = str(user_obj.pk)
            refresh.payload["account_type"] = str(user_obj.account_type)
            return Response(
                {"new_access_token": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_user_details(request):
    token = request.data.get("token")
    if token is not None:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

    user_id = decoded.get("user_id")
    account_type = decoded.get("account_type")

    if account_type == "EMP":
        employee_details = EmployeeDetailSerializer(
            EmployeeDetail.objects.get(account_id=user_id)
        ).data
        return Response(employee_details, status=status.HTTP_200_OK)
    elif account_type == "STU":
        student_details = StudentDetailSerializer(
            StudentDetail.objects.get(account_id=user_id)
        ).data
        return Response(student_details, status=status.HTTP_200_OK)
    elif account_type == "PAR":
        parent_details = ParentDetailSerializer(
            ParentDetail.objects.get(account_id=user_id)
        ).data
        return Response(parent_details, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "invalid_account_type"}, status=status.HTTP_400_BAD_REQUEST
        )
