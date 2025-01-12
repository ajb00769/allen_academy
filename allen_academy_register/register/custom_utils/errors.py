"""
These error messages exist for development-related errors such as when the frontend
developer was unable to pass the correct arguments into the API's parameters or when
a required parameter was not given any input.
"""

NULL_ARGS_ERROR = {
    "error": "No argument passed for a required parameter. Contact the developer with the error code.",
    "error_code": "AAR-00001",
}

INVALID_ARGS_ERROR = {
    "error": "Invalid arguments passed. Contact the developer with the error code.",
    "error_code": "AAR-00002",
}

EMAIL_ALREADY_REGISTERED_ERROR = {
    "error": "Email already registered with an existing user.",
    "error_code": "AAR-00003",
}

KEY_TYPE_VALUE_ERROR = {
    "error": "Value not valid for this particular key type.",
    "error_code": "AAR-00004",
}

DATA_DOES_NOT_MATCH_ERROR = {
    "error": "Data stored in the registration key does not match data in the payload.",
    "error_code": "AAR-00005",
}

STUDENT_DOES_NOT_EXIST = {
    "error": "Student refrenced does not exist.",
    "error_code": "AAR-00006",
}

UNEXPECTED_ERROR = {
    "error": "Something unexpected went wrong. Please contact the developer.",
    "error_code": "AAR-99999",
}
