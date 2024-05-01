from rest_framework.reponse import Response
from rest_framework_simplejwt import api_view

# Create your views here.

@api_view(["POST"])
def enroll(request):
    return Response({"success": True}, status=200)
