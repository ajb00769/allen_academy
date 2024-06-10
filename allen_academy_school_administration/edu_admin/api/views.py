from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["POST"])
def create_department(request):
    return Response({"success": True}, status=200)


@api_view(["POST"])
def create_course(request):
    return Response({"success": True}, status=200)


@api_view(["POST"])
def create_subject(request):
    return Response({"success": True}, status=200)


@api_view(["POST"])
def create_schedule(request):
    return Response({"success": True}, status=200)


@api_view(["POST", "PUT"])
def update_salary(request):
    return Response({"success": True}, status=200)
