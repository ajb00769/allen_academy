from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .serializers import RegistrationKeySerializer
from ..custom import generate_registration_key, date_time_handler
from ..models import RegistrationKey


@api_view(["POST"])
def register(request):
    pass


@api_view(["POST"])
def reg_key(request):
    with transaction.atomic():
        new_key = generate_registration_key()
        while new_key in RegistrationKey.objects.values_list(
            "generated_key", flat=True
        ):
            new_key = generate_registration_key()

        client_data = request.data.copy()
        server_data = {
            "generated_key": new_key,
            "key_expiry": date_time_handler(format="key_expiry"),
        }

        combined = {**client_data, **server_data}

        new_key_serializer = RegistrationKeySerializer(data=combined)
        if new_key_serializer.is_valid():
            new_key_serializer.save()
            return Response(new_key_serializer, status=201)
        return Response(new_key_serializer.errors, status=400)
