from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .custom import phone_validator
from .models import StudentDetail


class RegKeyTests(APITestCase):
    def setUp(self):
        self.url = reverse("reg_key")
        self.generated_for_default = "Potter Harry James"
        self.generated_for_minimum = "Li Max"
        self.generated_for_maximum = "Barnaby Marmaduke Aloysius Benjy Cobweb Dartagnan Egbert Felix Gaspar Humbert Ignatius Jayden Kasper Leroy Maximilian Neddy Obiajulu Pepin Quilliam Rosencrantz Sexton Teddy Upwood Vivatma Wayland Xylon Yardley Zachary Usansky  Aaron Bede Cedric Darius Eus"
        self.generated_for_spaces = "   Potter Harry    James"
        self.generated_for_invalid_too_long = "Barnaby Marmaduke Aloysius Benjy Cobweb Dartagnan Egbert Felix Gaspar Humbert Ignatius Jayden Kasper Leroy Maximilian Neddy Obiajulu Pepin Quilliam Rosencrantz Sexton Teddy Upwood Vivatma Wayland Xylon Yardley Zachary Usansky Aaron Bede Cedric Darius Eustace"
        self.generated_for_invalid_one_name = "Potter"
        self.default_key_type = "STU"
        self.all_valid_key_types = ["STU", "PAR", "EMP"]
        self.invalid_key_type = "123"

    def create_data(self, key_type=None, generated_for=None):
        data = {
            "key_type": key_type or self.default_key_type,
            "generated_for": generated_for or self.generated_for_default,
        }
        return data

    def test_null_args(self):
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_valid_args(self):
        for key_type in self.all_valid_key_types:
            with self.subTest():
                data = self.create_data(key_type=key_type)
                response = self.client.post(self.url, data, format="json")
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                keys_to_check = ["key_type", "generated_key", "key_expiry"]
                self.assertIn("key_type", response.data)
                self.assertIn("generated_key", response.data)
                self.assertIn("key_expiry", response.data)
                self.assertEqual(response.data.get("key_type"), data.get("key_type"))
                self.assertEqual(
                    response.data.get("generated_for"), data.get("generated_for")
                )
                self.assertEqual(response.data.get("key_used"), False)

    def test_gen_key_with_invalid_key_type(self):
        data = self.create_data(key_type=self.invalid_key_type)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gen_key_with_missing_args(self):
        data = self.create_data()
        data.pop("generated_for")
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_name_too_short(self):
        data = self.create_data(generated_for=self.generated_for_invalid_one_name)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_name_with_excess_spaces(self):
        data = self.create_data(generated_for=self.generated_for_spaces)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gen_key_with_key_used_true_arg(self):
        data = self.create_data()
        data.update({"key_used": True})
        response = self.client.post(self.url, data, format="json")
        self.assertIn("key_used", response.data)
        self.assertEqual(response.data.get("key_used"), False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ignore_manual_reg_key_injection(self):
        data = self.create_data()
        data.update({"generated_key": "this-key-is-invalid"})
        response = self.client.post(self.url, data, format="json")
        self.assertIn("generated_key", response.data)
        self.assertNotEqual(
            response.data.get("generated_key"), data.get("generated_key")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ignore_manual_key_expiry_injection(self):
        data = self.create_data()
        data.update({"key_expiry": "2091-01-01"})
        response = self.client.post(self.url, data, format="json")
        self.assertNotEqual(response.data.get("key_expiry"), data.get("key_expiry"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RegisterTests(APITestCase):
    def generate_args(self, key_type, gen_for):
        url = reverse("reg_key")
        data = {"key_type": key_type, "generated_for": gen_for}
        return self.client.post(url, data, format="json")

    def test_valid_registration_minimum(self):
        url = reverse("register")
        key_types = ["STU", "PAR", "EMP"]

        for key_type in key_types:
            args = self.generate_args(key_type, "Potter Harry")
            data = {
                "last_name": "Potter",
                "first_name": "Harry",
                "reg_key": args.data.get("generated_key"),
                "key_type": args.data.get("key_type"),
                "password": "1234",
                "email": "testemail@email.com",
                "address": "test address",
                "birthday": "1997-05-06",
                "phone": "+1800123456789",
            }
            if key_type == "PAR":
                student = StudentDetail.objects.values_list(
                    "account_id", flat=True
                ).first()
                data.update({"relationship": "R", "student": student})
            elif key_type == "EMP":
                data.update({"employment_type": "S"})

            response = self.client.post(url, data, format="json")
            self.assertEqual(response.data.get("success"), True)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_null_registration_args(self):
        url = reverse("register")
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_super_long_name(self):
        args = self.generate_args("STU", "Dela Cruz Juan Karlos Miguel Marquez JR")
        url = reverse("register")
        data = {
            "last_name": "Dela Cruz",
            "first_name": "Juan Karlos",
            "middle_name": "Miguel Marquez",
            "suffix": "JR",
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
            "password": "1234",
            "email": "testemail@email.com",
            "address": "test address",
            "birthday": "1997-05-06",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.data.get("success"), True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_phone_number(self):
        args = self.generate_args("PAR", "Potter Harry James")
        url = reverse("register")
        data = {
            "last_name": "Dela Cruz",
            "first_name": "Juan Karlos",
            "middle_name": "Miguel Marquez",
            "suffix": "JR",
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
            "password": "1234",
            "email": "testemail@email.com",
            "address": "test address",
            "birthday": "1997-05-06",
        }

    def test_missing_address(self):
        pass

    def test_missing_reg_key(self):
        pass

    def test_invalid_reg_key(self):
        pass

    def test_invalid_suffix(self):
        pass

    def test_invalid_emp_type(self):
        pass


class HelperFunctionTests(APITestCase):
    def test_string_sanitizer(self):
        pass

    def test_get_age_function(self):
        pass

    def test_validate_registration_key(self):
        pass

    def test_save_account_id(self):
        pass


if __name__ == "__main__":
    import django

    django.setup()
    APITestCase.run()
