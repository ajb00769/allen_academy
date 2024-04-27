from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
from register.models import AllAccount
from register.api.serializers import AllAccountSerializer


@api_view(["POST"])
def login(request):
    credentials = {
        "email": request.data.get("email"),
        "password": request.data.get("password"),
    }
    try:
        # user = account_model.objects.get(email=email)
        # if user.check_password(raw_password=password):
        #     return Response({"success": True}, status=200)
        db_fetched = AllAccount.objects.get(email=credentials.get("email"))
        checker = db_fetched.check_password(credentials.get("password"))
        if checker:
            return Response({"success": checker}, status=200)
        return Response({"success": checker}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
