from register.models import AllAccount


def is_user_account_active(user_id: str) -> bool:
    try:
        user_obj = AllAccount.objects.get(account_id=user_id)
        return user_obj.is_active
    except Exception:
        return False
