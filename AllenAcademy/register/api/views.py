from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from ..models import (
    AllAccountId,
    StudentAccount,
    ParentAccount,
    EmployeeAccount,
    RegistrationKey,
)
from ..custom import generate_account_id, generate_registration_key


@api_view(["POST"])
def register(request):
    pass
    # all_account_id_counts = AllAccountId.objects.filter(
    #     generated_id__startswith=current_year
    # ).count()

    # new_id = generate_account_id(all_account_id_counts)
    # save_new_id = AllAccountId(generated_id=new_id)
    # save_new_id.save()

    # get_fk = AllAccountId.objects.filter(generated_id=new_id)


@api_view(["POST"])
def reg_key(request):
    new_key = generate_registration_key()
    # if new_key not in RegistrationKey.objects.filter(generated_key=new_key):
    # return new_key
    return Response({"key": new_key})
