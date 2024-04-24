from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
from register.models import (
    RegistrationKey,
    AllAccountId,
    StudentAccount,
    ParentAccount,
    EmployeeAccount,
)
from register.api.serializers import (
    RegistrationKeySerializer,
    AccountIdSerializer,
    StudentAccountSerializer,
    StudentDetailSerializer,
    EmployeeAccountSerializer,
    EmployeeDetailSerializer,
    ParentAccountSerializer,
    ParentDetailSerializer,
)
from register.custom_utils.custom import (
    generate_registration_key,
    generate_account_id,
    date_time_handler,
)
from register.custom_utils.errors import (
    NULL_ARGS_ERROR,
    INVALID_ARGS_ERROR,
    UNEXPECTED_ERROR,
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
    invalid or NULL key types. Valid key_type will then be assigned to a
    dict for input validation into the db.
    """
    gen_for_list = [
        clean_excess_spaces_from_string(request.data.get("last_name")),
        clean_excess_spaces_from_string(request.data.get("first_name")),
        clean_excess_spaces_from_string(request.data.get("middle_name")),
        clean_excess_spaces_from_string(request.data.get("suffix")),
    ]  # sanitize input in case middle_name or suffix is null for null safety
    gen_for: str = remove_nulls_and_empty_strings(gen_for_list)
    key_type: str = request.data.get("key_type")

    if not key_type or not gen_for:
        return Response(NULL_ARGS_ERROR, status=400)

    if key_type not in serializer_map:
        timestamp = date_time_handler(format="timestamp")
        logger.warning(f"[{timestamp}]{func_name}: Invalid key type was passed.")
        return Response(INVALID_ARGS_ERROR, status=400)

    # declare all variables to be used in the transaction

    for_reg_key_validation = {
        "reg_key": request.data.get("reg_key"),
        "gen_for": gen_for,
        "key_type": key_type,
    }

    account_serializer_class, detail_serializer_class = serializer_map[key_type]
    account_class = model_map[key_type]

    new_account_id: str = generate_account_id(get_current_account_id_counts())

    try:
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
            validate_reg_key = validate_registration_key(for_reg_key_validation)
            if isinstance(validate_reg_key, dict):
                return Response(validate_reg_key, status=400)

            saved_account_id = save_account_id(account_id=new_account_id)
            if isinstance(saved_account_id, dict):
                return Response(saved_account_id, status=400)

            account_serializer_data = request.data.copy()
            account_serializer_data.update(
                {
                    "account_id": saved_account_id,
                    "password": make_password(account_serializer_data.get("password")),
                }
            )
            account_serializer = account_serializer_class(data=account_serializer_data)

            if not account_serializer.is_valid():
                raise Exception(account_serializer.errors)
            account_serializer.save()

            # Populate the AccountDetail table
            account_object = account_class.objects.get(
                account_id=account_serializer.data.get("account_id")
            )
            detail_serializer_data = request.data.copy()
            detail_serializer_data.update({"account_id": account_object.account_id})
            detail_serializer = detail_serializer_class(data=detail_serializer_data)

            if not detail_serializer.is_valid():
                raise Exception(detail_serializer.errors)
            detail_serializer.save()

            return Response({"success": True}, status=201)
    except Exception as e:
        return handle_exception(e, func_name=func_name)


@api_view(["POST"])
def reg_key(request):
    func_name = reg_key.__name__

    client_data = request.data.copy()
    client_data.pop("key_used", None)

    gen_for: str = clean_excess_spaces_from_string(client_data.get("generated_for"))

    if not gen_for or not client_data.get("key_type"):
        return Response(NULL_ARGS_ERROR, status=400)

    if len(gen_for.split()) < 2:
        return Response({"error": "Name too short."}, status=400)

    try:
        new_key: str = generate_registration_key()

        while new_key in RegistrationKey.objects.values_list(
            "generated_key", flat=True
        ):
            new_key: str = generate_registration_key()

        client_data.update(
            {
                "generated_key": new_key,
                "key_expiry": date_time_handler(format="key_expiry"),
                "generated_for": gen_for,
            }
        )

        new_key_serializer = RegistrationKeySerializer(data=client_data)

        with transaction.atomic():
            if new_key_serializer.is_valid():
                new_key_serializer.save()
                return Response(new_key_serializer.data, status=201)
            raise Exception(new_key_serializer.errors)
    except Exception as e:
        return handle_exception(e, func_name=func_name)


#########################################################################
#                   *** Helper Functions Section ***                    #
# /*-----------------------------------------------------------------*\ #
# I have decided to just add some of these functions within the same    #
# file because of their close-relationship with the views. Also, these  #
# functions use the same imports as the views and I wouldn't want to    #
# re-import the same items in the custom.py file again.                 #
#########################################################################


def save_account_id(account_id: str, max_retries=3) -> dict | str:
    """
    Returns a str with the account_id if saving is successful, otherwise
    returns a dict with an "error" key.
    """
    func_name = save_account_id.__name__

    account_id_serializer = AccountIdSerializer(data={"generated_id": account_id})

    for attempt in range(max_retries):
        try:
            with transaction.atomic():
                if attempt > 0:
                    account_id: str = generate_account_id(
                        get_current_account_id_counts()
                    )

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
            timestamp = date_time_handler(format="timestamp")
            logger.error(f"[{timestamp}]{func_name}: Unexpected error occured.")
            return {
                "error": f"Unexpected behavior. Please contact the developer and provide detailed steps that brought you to this point with this timestamp: {timestamp}."
            }


def validate_registration_key(data: dict) -> dict | int:
    """
    No other exceptions expected to happen in this helper function since the only
    point of failure would be getting a null reg_key_object if they reg_key argument
    does not exist in the db.

    The rest of the operations involve comparing data fetched from the db vs input.
    Returns an int = 0 if successful, returns a dict with and "error" key if not.
    """
    func_name = validate_registration_key.__name__

    reg_key: str = data.get("reg_key")

    # Terminate the function early if the key does not exist
    try:
        reg_key_object = RegistrationKey.objects.get(generated_key=reg_key)
    except RegistrationKey.DoesNotExist:
        return {"error": "Invalid key."}

    # Terminate the function early if key is for another account type
    if reg_key_object.key_type != data.get("key_type"):
        return {"error": "Key type is for a different account type."}

    reg_key_errors = []

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

    gen_for: str = data.get("gen_for")

    if reg_key_object.generated_for != gen_for:
        timestamp = date_time_handler(format="timestamp")
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


def handle_exception(e: Exception, func_name: str) -> Response:
    timestamp = date_time_handler(format="timestamp")
    if isinstance(e.args[0], dict):
        err_key = next(iter(e.args[0]))
        logger.error(
            f"[{timestamp}]{func_name}: Parameter {err_key}: {e.args[0].get(err_key)[0]}"
        )
        return Response(NULL_ARGS_ERROR, status=400)
    logger.error(f"[{timestamp}]{func_name}: {e}")
    return Response(UNEXPECTED_ERROR, status=400)


def clean_excess_spaces_from_string(string: str | None) -> str:
    """
    Includes a None type as an input parameter since some of the inputs are
    optional in the data model.
    """
    if string is None:
        return None
    removed_spaces = [i for i in string.split() if i]
    return " ".join(removed_spaces)


def remove_nulls_and_empty_strings(input: list) -> str:
    return " ".join([i for i in input if i])


def get_current_account_id_counts() -> int:
    current_year = date_time_handler(format="year")
    return AllAccountId.objects.filter(generated_id__startswith=current_year).count()
