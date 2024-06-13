from rest_framework.response import Response
from rest_framework.decorators import api_view
from login.api.serializers import CustomTokenObtainPairSerializer


@api_view(["POST"])
def login(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=200)
    return Response(serializer.errors, status=400)
