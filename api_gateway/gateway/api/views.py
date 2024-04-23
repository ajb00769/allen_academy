from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DynamicModelSerializer

# Create your views here.


@api_view(["POST"])
def test(request):
    pass
