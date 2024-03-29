from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
from ..custom import (
    generate_registration_key,
    generate_account_id,
    date_time_handler,
)
from ..models import (
    RegistrationKey,
    AllAccountId,
    StudentAccount,
    ParentAccount,
    EmployeeAccount,
)
import logging


# Initialize logger
logger = logging.getLogger(__name__)


@api_view(["POST"])
def register(request):
    """
    Expecting a key type and registration key input from client
    that was generated previously in reg_key api.
    """

    func_name = register.__name__

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

    """
    Validate key_type before anything else, early program termination for
    invalid key types. Valid key_type will then be assigned to a dict for
    input validation into the db.
    """
    key_type = request.data.get("key_type")
    if key_type not in serializer_map:
        timestamp = date_time_handler(format="timestamp")
        logger.warning(f"[{timestamp}]{func_name}: Invalid key type was passed.")
        return Response({"error": "Invalid key type."}, status=400)

    for_reg_key_validation = {
        "reg_key": request.data.get("reg_key"),
        "gen_for": [
            request.data.get("last_name"),
            request.data.get("first_name"),
            request.data.get("middle_name"),
            request.data.get("suffix"),
        ],
        "key_type": key_type,
    }

    account_serializer_class, detail_serializer_class = serializer_map[key_type]
    account_class = model_map[key_type]

    # Get the initial counts and generate the initial account id
    current_id_counts = AllAccountId.objects.all().count()
    new_account_id = generate_account_id(current_id_counts)

    with transaction.atomic():
        """
        All operations that involve altering or inserting data into the db will be
        placed within the scope of transaction.atomic to treat it as a single
        transaction.
        
        The validate_registration_key function alters the key_used column of a key
        making it unusable afterwards. If this is done outside of the scope of
        transaction.atomic if the succeeding operations fail an account will not
        be created but the registration key will become unusable.
        """
        validate_reg_key = validate_registration_key(for_reg_key_validation).get(
            "error"
        )
        if validate_reg_key:
            return Response({"error": validate_reg_key}, status=400)

        saved_account_id = save_account_id(account_id=new_account_id)
        if isinstance(saved_account_id, dict):
            return Response({"error": saved_account_id.get("error")}, status=400)

        # Get the id object from AllAccountId to plug into the OneToOne account_id field
        all_account_id_object = AllAccountId.objects.get(generated_id=saved_account_id)
        account_serializer_data = request.data.copy()
        account_serializer_data.update(
            {
                "account_id": all_account_id_object.generated_id,
                "password": make_password(account_serializer_data.get("password")),
            }
        )
        account_serializer = account_serializer_class(data=account_serializer_data)

        if not account_serializer.is_valid():
            return Response(account_serializer.errors, status=400)
        account_serializer.save()

        # Populate the AccountDetail table
        account_object = account_class.objects.get(
            account_id=account_serializer.data.get("account_id")
        )
        detail_serializer_data = request.data.copy()
        detail_serializer_data.update({"account_id": account_object.account_id})
        detail_serializer = detail_serializer_class(data=detail_serializer_data)

        if not detail_serializer.is_valid():
            return Response(detail_serializer.errors, status=400)
        detail_serializer.save()

        return Response({"result": True}, status=201)


@api_view(["POST"])
def reg_key(request):
    func_name = reg_key.__name__

    client_data = request.data.copy()

    try:
        new_key = generate_registration_key()

        while new_key in RegistrationKey.objects.values_list(
            "generated_key", flat=True
        ):
            new_key = generate_registration_key()

        client_data.update(
            {
                "generated_key": new_key,
                "key_expiry": date_time_handler(format="key_expiry"),
            }
        )

        new_key_serializer = RegistrationKeySerializer(data=client_data)

        with transaction.atomic():
            if new_key_serializer.is_valid():
                new_key_serializer.save()
                return Response(new_key_serializer.data, status=201)
            return Response(new_key_serializer.errors, status=400)
    except Exception as e:
        timestamp = date_time_handler(format="timestamp")
        logger.exception(
            f"[{timestamp}]{func_name}: An error occured while creating the registration key. {e}"
        )
        return Response(
            {"error": "An error occured while creating the registratoin key."}
        )


#########################################################################
#                   *** Helper Functions Section ***                    #
# /*-----------------------------------------------------------------*\ #
# I have decided to just add some of these functions within the same    #
# file because of their clos-relationship with the views. Also, these   #
# functions use the same imports as the views and I wouldn't want to    #
# re-import the same items in the custom.py file again.                 #
#########################################################################


def save_account_id(account_id, max_retries=3):
    func_name = save_account_id.__name__

    account_id_serializer = AccountIdSerializer(data={"generated_id": account_id})

    for attempt in range(max_retries):
        try:
            with transaction.atomic():
                if attempt > 0:
                    current_year = date_time_handler(format="year")
                    current_id_counts = AllAccountId.objects.filter(
                        generated_id__startswith=current_year
                    ).count()
                    account_id = generate_account_id(current_id_counts)

                if isinstance(account_id, dict):
                    account_id_err_msg = account_id.get("error")
                    timestamp = date_time_handler(format="timestamp")
                    logger.error(f"[{timestamp}]{func_name}: {account_id_err_msg}")
                    return {"error": account_id_err_msg}

                if account_id_serializer.is_valid():
                    account_id_serializer.save()
                    return account_id_serializer.data.get("generated_id")
        except IntegrityError:
            timestamp = date_time_handler(format="timestamp")
            logger.exception(
                f"[{timestamp}]{func_name}: Failed to save new account id: {account_id} id already exists. Attempt: {attempt + 1} of {max_retries}."
            )
            if attempt == max_retries - 1:
                logger.warning(
                    f"[{timestamp}]{func_name}: Account ID creation error more than 3 attempts to create account ID but all failed. Consider checking the table."
                )
                return ValidationError(
                    {
                        "error": "Unable to create new account id. Please try again later."
                    }
                )
        else:
            logger.error(f"[{timestamp}]{func_name}: Unhandled error occured.")
            return {
                "error": "Unexpected behavior. Please contact the administrator and provide detailed steps that brought you to this point."
            }


def validate_registration_key(data):
    func_name = validate_registration_key.__name__

    reg_key = data.get("reg_key")

    # Terminate the function early if the key does not exist
    try:
        reg_key_object = RegistrationKey.objects.get(generated_key=reg_key)
    except ObjectDoesNotExist:
        return {"error": "Invalid key."}

    # Terminate the function early if key is for another account type
    if reg_key_object.key_type != data.get("key_type"):
        return {"error": "Key type is for a different account type."}

    reg_key_errors = []
    # Sanitize None or empty string for suffix and middle name
    gen_for_sanitized = [i for i in data.get("gen_for") if i]
    gen_for = " ".join(gen_for_sanitized)

    if reg_key_object.key_expiry <= date_time_handler("date"):
        timestamp = date_time_handler(format="timestamp")
        logger.exception(
            f"[{timestamp}]{func_name}: An expired key was attempted to be registered belonging to: {reg_key_object.generated_for}."
        )
        reg_key_errors.append("Key already expired, please request a new key.")

    if reg_key_object.key_used:
        timestamp = date_time_handler(format="timestamp")
        logger.warning(
            f"[{timestamp}]{func_name}: Someone attempted to register with a used key: {reg_key_object.generated_key}."
        )
        reg_key_errors.append("Key already used.")

    if reg_key_object.generated_for != gen_for:
        logger.exception(
            f"[{timestamp}]{func_name}: User attempted to use registration key {reg_key} for {gen_for}. If user complains please check the db for the key's owner."
        )
        return {"error": "Key is not intended for this person."}

    if (
        reg_key_object is not None
        and reg_key_object.generated_for == gen_for
        and not reg_key_errors
    ):
        reg_key_object.key_used = True
        reg_key_object.save()
        return 0

    reg_key_errors.append("Registration error.")
    return {
        "error": " ".join(reg_key_errors),
    }
