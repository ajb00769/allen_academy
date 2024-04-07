"""
These error messages exist for development-related errors such as when the frontend
developer was unable to pass the correct arguments into the API's parameters or when
a required parameter was not given any input.
"""

NULL_ARGS_ERROR = {
    "error": "No argument passed for a required parameter. Contact the developer with the error code.",
    "error_code": "AAR-00001",
}

INVALID_KEY_TYPE_ERROR = {
    "error": "Invalid key type. Contact the developer with the error code.",
    "error_code": "AAR-00002",
}

UNEXPECTED_ERROR = {
    "error": "Something unexpected went wrong. Please contact the developer.",
    "error_code": "AAR-99999",
}
