from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegKeyTests(APITestCase):
    def test_null_args(self):
        url = reverse("reg_key")
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_valid_args(self):
        url = reverse("reg_key")
        pass

    def test_gen_key_with_invalid_args(self):
        url = reverse("reg_key")
        data = {"key_type": "123", "generated_for": "Harry Potter"}
        response = self.client.post(url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_missing_args(self):
        url = reverse("reg_key")
        data = {"key_type": "STU"}
        response = self.client.post(url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_name_too_short(self):
        url = reverse("reg_key")
        data = {"key_type": "STU", "generated_for": "Harry"}
        response = self.client.post(url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_name_with_excess_spaces(self):
        url = reverse("reg_key")
        data = {"key_type": "STU", "generated_for": "  Harry  Potter "}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gen_key_with_key_used_true_arg(self):
        url = reverse("reg_key")
        data = {
            "key_used": True,
            "generated_for": "Harry Potter",
            "key_type": "STU",
        }
        response = self.client.post(url, data, format="json")
        self.assertIn("key_used", response.data)
        self.assertEqual(response.data.get("key_used"), False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ignore_manual_reg_key_injection(self):
        url = reverse("reg_key")
        data = {
            "generated_key": "this-key-is-invalid",
            "generated_for": "Harry Potter",
            "key_type": "STU",
        }
        response = self.client.post(url, data, format="json")
        self.assertIn("generated_key", response.data)
        self.assertNotEqual(
            response.data.get("generated_key"), data.get("generated_key")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ignore_manual_key_expiry_injection(self):
        url = reverse("reg_key")
        data = {
            "generated_for": "Harry Potter",
            "key_type": "STU",
            "key_expiry": "2091-01-01",
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.data.get("key_expiry"), data.get("key_expiry"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RegisterTests(APITestCase):
    def test_successful_reg_key_purged(self):
        # a successful registration should purge the used key
        pass
