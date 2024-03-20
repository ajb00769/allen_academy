from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .serializers import (
    RegistrationKeySerializer,
    AccountIdSerializer,
    StudentAccountSerializer,
    StudentDetailSerializer,
    EmployeeAccountSerializer,
    EmployeeDetailSerializer,
    ParentAccountSerializer,
    ParentDetailSerializer,
)
from ..custom import generate_registration_key, date_time_handler, generate_account_id
from ..models import (
    RegistrationKey,
    AllAccountId,
    StudentAccount,
    ParentAccount,
    EmployeeAccount,
)


@api_view(["POST"])
def register(request):
    """
    Expecting a key type and registration key input from client
    that was generated previously in reg_key api.
    """
    serializer_map = {
        "STU": (StudentAccountSerializer, StudentDetailSerializer),
        "PAR": (ParentAccountSerializer, ParentDetailSerializer),
        "EMP": (EmployeeAccountSerializer, EmployeeDetailSerializer),
    }

    model_map = {
        "STU": StudentAccount,
        "PAR": ParentAccount,
        "EMP": EmployeeAccount,
    }

    for_reg_key_validation = {
        "reg_key": request.data.get("reg_key"),
        "gen_for": [
            request.data.get("last_name"),
            request.data.get("first_name"),
            request.data.get("middle_name"),
            request.data.get("suffix"),
        ],
    }

    validate_reg_key = validate_registration_key(for_reg_key_validation).get("error")
    if not validate_reg_key:
        return Response({"error": validate_reg_key}, status=400)

    key_type = request.data.get("key_type")
    if key_type not in serializer_map:
        return Response({"error": "Invalid key type."}, status=400)

    account_serializer_class, detail_serializer_class = serializer_map[key_type]
    account_class = model_map[key_type]

    # Generate a new account id and save into AllAccountId table
    current_id_counts = AllAccountId.objects.all().count()
    new_account_id = generate_account_id(current_id_counts)
    saved_account_id = save_account_id(account_id=new_account_id)
    if saved_account_id is None:
        return Response(
            {"error": "Unable to create an account id. Please try again later"},
            status=400,
        )

    with transaction.atomic():
        # Get the id object from AllAccountId to plug into the OneToOne account_id field
        all_account_id_object = AllAccountId.objects.get(generated_id=saved_account_id)
        account_serializer_data = request.data.copy()
        account_serializer_data.update(
            {
                "account_id": all_account_id_object.generated_id,
            }
        )
        account_serializer = account_serializer_class(data=account_serializer_data)

        if not account_serializer.is_valid():
            return Response(account_serializer.errors, status=400)
        account_serializer.save()

        # Populate the AccountDetail table
        account_object = account_class.objects.get(
            account_id=account_serializer.data["account_id"]
        )
        detail_serializer_data = request.data.copy()
        detail_serializer_data.update(
            {
                "account_id": account_object.account_id,
            }
        )
        detail_serializer = detail_serializer_class(data=detail_serializer_data)

        if not detail_serializer.is_valid():
            return Response(detail_serializer.errors, status=400)
        detail_serializer.save()

        return Response({"result": True}, status=201)


@api_view(["POST"])
def reg_key(request):
    with transaction.atomic():
        client_data = request.data.copy()
        new_key = generate_registration_key()

        while new_key in RegistrationKey.objects.values_list(
            "generated_key", flat=True
        ):
            new_key = generate_registration_key()

        server_data = {
            "generated_key": new_key,
            "key_expiry": date_time_handler(format="key_expiry"),
        }

        combined = {**client_data, **server_data}

        new_key_serializer = RegistrationKeySerializer(data=combined)
        if new_key_serializer.is_valid():
            new_key_serializer.save()
            return Response(new_key_serializer.data, status=201)
        return Response(new_key_serializer.errors, status=400)


#########################################################################
#                   *** Helper Functions Section ***                    #
# /*-----------------------------------------------------------------*\ #
# I have decided to just add some of these functions within the same    #
# file because of their clos-relationship with the views. Also, these   #
# functions use the same imports as the views and I wouldn't want to    #
# re-import the same items in the custom.py file again.                 #
#########################################################################


def save_account_id(account_id, max_retries=3):
    account_id_serializer = AccountIdSerializer(data={"generated_id": account_id})
    for attempt in range(max_retries):
        try:
            with transaction.atomic():
                if attempt > 0:
                    current_id_counts = AllAccountId.objects.all().count()
                    account_id = generate_account_id(current_id_counts)

                if account_id_serializer.is_valid():
                    account_id_serializer.save()
                    return account_id_serializer.data["generated_id"]
        except IntegrityError:
            print(
                "Failed to save new account id, id already exists."
                + f"\nAttempt: {attempt + 1} of {max_retries}."
            )
            if attempt == max_retries - 1:
                raise ValidationError(
                    "Unable to create new account id. Please try again later."
                )


def validate_registration_key(data):
    reg_key = data["reg_key"]
    gen_for_sanitized = [i for i in data["gen_for"] if i]
    gen_for = " ".join(gen_for_sanitized)

    reg_key_object = RegistrationKey.objects.get(generated_key=reg_key)

    if reg_key_object.key_expiry >= date_time_handler("date"):
        return {
            "error": "Key Error: already expired. Please request for a new key.",
        }  # key already expired

    if reg_key_object.key_used:
        return {
            "error": "Key Error: already used.",
        }  # key already used

    if reg_key_object is not None and reg_key_object.generated_for == gen_for:
        reg_key_object.key_used = True
        reg_key_object.save()
        return {
            "success": True,
        }
    return {
        "error": "Key Error: does not exist or does not match the name.",
    }
