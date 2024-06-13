from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from custom_common.jwt_handler import handle_jwt


@api_view(["POST"])
def create_department(request):
    result = handle_jwt(request)

    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)
    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_course(request):
    result = handle_jwt(request)

    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)
    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_subject(request):
    result = handle_jwt(request)

    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)
    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_schedule(request):
    result = handle_jwt(request)

    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)
    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST", "PUT"])
def update_salary(request):
    result = handle_jwt(request)

    if "error" in result:
        return Response(result, status=status.HTTP_403_FORBIDDEN)
    return Response(result, status=status.HTTP_200_OK)
