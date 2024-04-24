from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
from register.models import StudentAccount, EmployeeAccount, ParentAccount


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    account_type = request.data.get("account_type")
    account_type_map = {
        "STU": StudentAccount,
        "EMP": EmployeeAccount,
        "PAR": ParentAccount,
    }
    account_model = account_type_map[account_type]
    try:
        user = account_model.objects.get(email=email)
        if user.check_password(password):
            return Response({"success": True}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
