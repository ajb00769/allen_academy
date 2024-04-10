from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegKeyTests(APITestCase):

    def test_null_params(self):
        url = reverse("reg_key")
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_valid_args(self):
        url = reverse("reg_key")
        pass

    def test_gen_key_with_invalid_args(self):
        url = reverse("reg_key")
        data = {"key_type": "123", "generated_for": "Harry Potter"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_incomplete_args(self):
        url = reverse("reg_key")
        # must reject if incomplete arguments
        pass

    def test_gen_key_with_key_used_true_arg(self):
        url = reverse("reg_key")
        # must not accept key_used true
        pass


class RegisterTests(APITestCase):
    def test_successful_reg_key_purged(self):
        # a successful registration should purge the used key
        pass
