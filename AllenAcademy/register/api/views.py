from rest_framework.response import Response
from rest_framework.decorators import api_view

# from register.models import AllAccountIds
# from .serializers import AccountIdSerializer


@api_view(["GET"])
def index(request):
    obj = {"name": "Register API"}
    return Response(obj)
