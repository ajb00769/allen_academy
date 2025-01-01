from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from register.models import (
    RegistrationKey,
    AllAccountId,
    AllAccount,
    StudentDetail,
)
from register.api.serializers import (
    RegistrationKeySerializer,
    AccountIdSerializer,
    AllAccountSerializer,
    StudentDetailSerializer,
    EmployeeDetailSerializer,
    ParentDetailSerializer,
)
from register.custom_utils.custom import (
    generate_registration_key,
    generate_account_id,
    date_time_handler,
)
from custom_common.jwt_handler import handle_jwt
from register.custom_utils.errors import (
    NULL_ARGS_ERROR,
    INVALID_ARGS_ERROR,
    EMAIL_ALREADY_REGISTERED_ERROR,
    KEY_TYPE_VALUE_ERROR,
    DATA_DOES_NOT_MATCH_ERROR,
    STUDENT_DOES_NOT_EXIST,
    UNEXPECTED_ERROR,
)
from register.custom_utils.constants import (
    ELEMENTARY_SCHOOL_CHOICES,
    MIDDLE_SCHOOL_CHOICES,
    HIGH_SCHOOL_CHOICES,
    COLLEGE_LEVEL_CHOICES,
    LAW_CHOICES,
    MASTERS_CHOICES,
    PHD_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES,
    FAMILY_TYPE_CHOICES,
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

    """
    # BUGFIX: K61Z8Sna - FIXED
    Function/view did not previously check if email is already registered.
    Although the data model/db has as unique restraint for the username/email
    it would inefficient to allow the operation to continue before that happens
    so early termination of the operation/error feedback is added.

    NOTE: noticed something that might be an issue where if the wrong year_level
    is entered in reg_key and is attempted to be registered, this function will
    return an error about a required field being missing but it's actually a
    rejection of the invalid year_level - account_type relationship.
    """
    email = clean_excess_spaces_from_string(request.data.get("email"))

    try:
        if AllAccount.objects.get(email=email):
            return Response(EMAIL_ALREADY_REGISTERED_ERROR, status=400)
    except ObjectDoesNotExist:
        pass

    serializer_map = {
        "STU": StudentDetailSerializer,
        "PAR": ParentDetailSerializer,
        "EMP": EmployeeDetailSerializer,
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

    detail_serializer_class = serializer_map[key_type]

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
            validated_reg_key = validate_registration_key(for_reg_key_validation)
            if validated_reg_key.get("error"):
                return Response(validated_reg_key.get("error"), status=400)

            saved_account_id = save_account_id(account_id=new_account_id)
            if isinstance(saved_account_id, dict):
                return Response(saved_account_id, status=400)

            account_serializer_data = request.data.copy()
            account_serializer_data.update(
                {
                    "account_id": saved_account_id,
                    "username": email,
                    "password": make_password(account_serializer_data.get("password")),
                    "account_type": key_type,
                }
            )
            if key_type == "PAR":
                try:
                    stored_relationship = RegistrationKey.objects.get(
                        year_level=request.data.get("year_level")
                    ).year_level

                    if request.data.get("year_level") != stored_relationship:
                        reg_key_obj = RegistrationKey.objects.get(
                            generated_key=request.data.get("reg_key")
                        )
                        reg_key_obj.key_used = False
                        reg_key_obj.save()
                        return Response(DATA_DOES_NOT_MATCH_ERROR, status=400)
                except ObjectDoesNotExist:
                    return Response(NULL_ARGS_ERROR, status=400)
            if key_type == "EMP":
                try:
                    stored_teaching_year_lvl = RegistrationKey.objects.get(
                        generated_key=request.data.get("reg_key")
                    )

                    if (
                        request.data.get("teaching_year_lvl")
                        != stored_teaching_year_lvl
                    ):
                        reg_key_obj = RegistrationKey.objects.get(
                            generated_key=request.data.get("reg_key")
                        )
                        reg_key_obj.key_used = False
                        reg_key_obj.save()
                        return Response(
                            {
                                "error": "Teaching year level stored in reg key does not match the teaching year level you submitted. Please select the correct teaching year level. If this is not correct please go to the registrar to confirm what year level you are teaching."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except ObjectDoesNotExist:
                    return Response(
                        {"error": "Registration key does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            account_serializer = AllAccountSerializer(data=account_serializer_data)

            if not account_serializer.is_valid():
                raise Exception(account_serializer.errors)
            account_serializer.save()

            # Populate the AccountDetail table
            account_object = AllAccount.objects.get(
                account_id=account_serializer.data.get("account_id")
            )
            detail_serializer_data = request.data.copy()
            if key_type == "STU":
                detail_serializer_data.update(
                    {"current_yr_lvl": validated_reg_key.get("year_level")}
                )
            elif key_type == "PAR":
                try:
                    student = StudentDetail.objects.get(
                        account_id=request.data.get("student")
                    )
                    detail_serializer_data.update({"student": student})
                except ObjectDoesNotExist:
                    return Response(STUDENT_DOES_NOT_EXIST, status=400)

                detail_serializer_data.update({"relationship": stored_relationship})

            detail_serializer_data.update({"account_id": account_object.account_id})
            detail_serializer = detail_serializer_class(data=detail_serializer_data)

            if not detail_serializer.is_valid():
                raise Exception(detail_serializer.errors)
            detail_serializer.save()

            return Response(detail_serializer.data, status=201)
    except Exception as e:
        reg_key_obj = RegistrationKey.objects.get(
            generated_key=request.data.get("reg_key")
        )
        reg_key_obj.key_used = False
        reg_key_obj.save()
        return handle_exception(e, func_name=func_name)


@api_view(["POST"])
def reg_key(request):
    func_name = reg_key.__name__

    client_data = request.data.copy()
    client_data.pop("key_used", None)
    client_data_key_type = clean_excess_spaces_from_string(client_data.get("key_type"))
    client_data_year_level = clean_excess_spaces_from_string(
        client_data.get("year_level")
    )

    gen_for: str = clean_excess_spaces_from_string(client_data.get("generated_for"))

    if not gen_for or not client_data_key_type or not client_data_year_level:
        return Response(NULL_ARGS_ERROR, status=400)

    if client_data_key_type == "STU":
        combined_type_list = (
            ELEMENTARY_SCHOOL_CHOICES
            + MIDDLE_SCHOOL_CHOICES
            + HIGH_SCHOOL_CHOICES
            + COLLEGE_LEVEL_CHOICES
            + LAW_CHOICES
            + MASTERS_CHOICES
            + PHD_CHOICES
        )
        if not any(item[0] == client_data_year_level for item in combined_type_list):
            return Response(KEY_TYPE_VALUE_ERROR, status=400)
    elif client_data_key_type == "EMP":
        if not any(
            item[0] == client_data_year_level for item in EMPLOYEE_YEAR_LEVEL_CHOICES
        ):
            return Response(KEY_TYPE_VALUE_ERROR, status=400)
    elif client_data_key_type == "PAR":
        if not any(item[0] == client_data_year_level for item in FAMILY_TYPE_CHOICES):
            return Response(KEY_TYPE_VALUE_ERROR, status=400)

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
                return Response(new_key_serializer.data, status=status.HTTP_201_CREATED)
            raise Exception(new_key_serializer.errors)
    except Exception as e:
        return handle_exception(e, func_name=func_name)


@api_view(["POST"])
def get_account_type_options(request):
    result = handle_jwt(request)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    account_type = request.data.get("key_type")

    if account_type == "STU":
        student_options = dict(
            ELEMENTARY_SCHOOL_CHOICES
            + MIDDLE_SCHOOL_CHOICES
            + HIGH_SCHOOL_CHOICES
            + COLLEGE_LEVEL_CHOICES
            + LAW_CHOICES
            + MASTERS_CHOICES
            + PHD_CHOICES
        )

        return Response(
            {"data": [{key: value} for key, value in student_options.items()]},
            status=status.HTTP_200_OK,
        )
    elif account_type == "EMP":
        return Response(
            {
                "data": [
                    {key: value}
                    for key, value in dict(EMPLOYEE_YEAR_LEVEL_CHOICES).items()
                ]
            },
            status=status.HTTP_200_OK,
        )
    elif account_type == "PAR":
        return Response(
            {
                "data": [
                    {key: value} for key, value in dict(FAMILY_TYPE_CHOICES).items()
                ]
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "invalid_account_type_regkey"}, status=status.HTTP_400_BAD_REQUEST
        )


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


def validate_registration_key(data: dict) -> dict | RegistrationKeySerializer:
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

    reg_key_serializer = RegistrationKeySerializer(reg_key_object)
    reg_key_data = reg_key_serializer.data

    # Terminate the function early if key is for another account type
    if reg_key_data.get("key_type") != data.get("key_type"):
        return {"error": "Key type is for a different account type."}

    reg_key_errors = []

    if reg_key_object.key_expiry <= date_time_handler("date"):
        timestamp = date_time_handler(format="timestamp")
        generated_for_err_field = reg_key_data.get("generated_for")
        logger.exception(
            f"[{timestamp}]{func_name}: An expired key was attempted to be registered belonging to: {generated_for_err_field}."
        )
        reg_key_errors.append("Key already expired, please request a new key.")

    if reg_key_data.get("key_used"):
        timestamp = date_time_handler(format="timestamp")
        generated_key_err_field = reg_key_data.get("generated_key")
        logger.warning(
            f"[{timestamp}]{func_name}: Someone attempted to register with a used key: {generated_key_err_field}."
        )
        reg_key_errors.append("Key already used.")

    gen_for: str = data.get("gen_for")

    if reg_key_data.get("generated_for") != gen_for:
        timestamp = date_time_handler(format="timestamp")
        logger.exception(
            f"[{timestamp}]{func_name}: User attempted to use registration key {reg_key} for {gen_for}. If user complains please check the db for the key's owner."
        )
        return {"error": "Key is not intended for this person."}

    if (
        reg_key_object is not None
        and reg_key_data.get("generated_for") == gen_for
        and not reg_key_errors
    ):
        reg_key_object.key_used = True
        reg_key_object.save()
        return reg_key_data

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
