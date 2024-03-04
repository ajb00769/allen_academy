from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def index(request):
    obj = {"name": "Register API"}
    return Response(obj)
