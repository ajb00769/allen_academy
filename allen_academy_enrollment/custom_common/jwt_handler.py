import jwt
from django.conf import settings
from custom_common.custom_auth import is_user_account_active


def handle_jwt(request) -> dict:
    try:
        if request.data.get("token") is None:
            return {"error": "no_token_supplied"}
        payload = jwt.decode(
            request.data.get("token"), settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )

        if not is_user_account_active(payload.get("user_id")):
            return {"error": "user_banned"}

        # only accept access tokens
        if payload.get("token_type") != "access":
            return {"error": "invalid_token_type"}
        return payload
    except jwt.exceptions.InvalidSignatureError:
        return {"error": "invalid"}
    except jwt.exceptions.ExpiredSignatureError:
        return {"error": "expired"}
    except jwt.DecodeError:
        return {"error": "decode_error"}
