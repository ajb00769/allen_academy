from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import StudentDetail


class RegKeyTests(APITestCase):
    def test_null_args(self):
        url = reverse("reg_key")
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_valid_args(self):
        url = reverse("reg_key")
        key_types = ["STU", "PAR", "EMP"]
        generated_for = "Harry James Potter"

        for key_type in key_types:
            data = {"key_type": key_type, "generated_for": generated_for}
            response = self.client.post(url, data, format="json")
            keys_to_check = ["key_type", "generated_key", "key_expiry"]

            for key in keys_to_check:
                self.assertIn(key, response.data)

            self.assertEqual(response.data.get("key_type"), data.get("key_type"))
            self.assertEqual(
                response.data.get("generated_for"), data.get("generated_for")
            )
            self.assertEqual(response.data.get("key_used"), False)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gen_key_with_invalid_key_type(self):
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
    def generate_args(self, key_type):
        url = reverse("reg_key")
        data = {"key_type": key_type, "generated_for": "Potter Harry James"}
        return self.client.post(url, data, format="json")

    def test_valid_registration(self):
        url = reverse("register")
        key_types = ["STU", "PAR", "EMP"]

        for key_type in key_types:
            args = self.generate_args(key_type)
            data = {
                "last_name": "Potter",
                "first_name": "Harry",
                "middle_name": "James",
                "reg_key": args.data.get("generated_key"),
                "key_type": args.data.get("key_type"),
                "password": "1234",
                "email": "testemail@email.com",
                "address": "test address",
                "birthday": "1997-05-06",
                "phone": "+1800123456789",
            }
            if key_type == "PAR":
                student = StudentDetail.objects.values("account_id").first()
                data.update({"relationship": "R", "student": student.get("account_id")})
            elif key_type == "EMP":
                data.update({"employment_type": "S"})

            response = self.client.post(url, data, format="json")
            self.assertEqual(response.data.get("success"), True)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class HelperFunctionTests(APITestCase):
    def test_validate_registration_key(self):
        pass

    def test_save_account_id(self):
        pass
