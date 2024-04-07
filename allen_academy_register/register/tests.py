from django.urls import reverse
from rest_framework.test import APITestCase


class RegKeyTests(APITestCase):
    def gen_key_with_valid_args(self):
        pass

    def gen_key_with_invalid_args(self):
        pass

    def gen_key_with_incomplete_args(self):
        # must reject if incomplete arguments
        pass

    def gen_key_with_key_used_true_arg(self):
        # must not accept key_used true
        pass


class RegisterTests(APITestCase):
    def successful_reg_key_purged(self):
        # a successful registration should purge the used key
        pass
