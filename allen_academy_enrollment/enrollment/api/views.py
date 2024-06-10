from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["POST"])
def enroll(request):
    return Response({"success": True}, status=200)
