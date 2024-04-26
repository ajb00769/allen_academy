from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.test import APITestCase
from register.api.views import validate_registration_key, save_account_id
from register.custom_utils.custom import phone_validator, generate_account_id
from register.models import StudentDetail, AllAccountId


class PhoneNumberValidationTests(APITestCase):
    def setUp(self):
        self.phone_validator = phone_validator

    def test_valid_phone_number(self):
        try:
            self.phone_validator("+12345678")
            self.phone_validator("+123456789098765")
        except ValidationError:
            self.fail("Valid phone number raised a ValidationError")

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            self.phone_validator("+1")
            self.phone_validator("+1234567")
            self.phone_validator("+1234567890987654")
            self.phone_validator("Hello, world!")


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

    def test_name_too_long(self):
        data = self.create_data(generated_for=self.generated_for_invalid_too_long)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shortest_valid_name(self):
        data = self.create_data(generated_for=self.generated_for_minimum)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_longest_valid_name(self):
        data = self.create_data(generated_for=self.generated_for_maximum)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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


class HelperFunctionTests(APITestCase):
    def setUp(self):
        self.url = reverse("reg_key")
        self.default_generated_for = "Potter Harry"
        self.default_key_type = "STU"

    def create_key(self, key_type=None, generated_for=None):
        data = {
            "key_type": key_type or self.default_key_type,
            "generated_for": generated_for or self.default_generated_for,
        }
        response = self.client.post(self.url, data, format="json")
        return response.data

    def test_validate_registration_key_valid(self):
        args = self.create_key()
        data = {
            "reg_key": args.get("generated_key"),
            "key_type": args.get("key_type"),
            "gen_for": self.default_generated_for,
        }
        result = validate_registration_key(data)
        self.assertEqual(result, 0)

    def test_validate_registration_key_invalid_key_type(self):
        args = self.create_key()
        data = {
            "reg_key": args.get("generated_key"),
            "key_type": "XX",
            "gen_for": self.default_generated_for,
        }
        result = validate_registration_key(data)
        self.assertIn("error", result)

    def test_validate_registration_key_mismatch_key_type(self):
        args = self.create_key()
        data = {
            "reg_key": args.get("generated_key"),
            "key_type": "EMP",
            "gen_for": self.default_generated_for,
        }
        result = validate_registration_key(data)
        self.assertIn("error", result)

    def test_validate_registration_key_invalid_reg_key(self):
        args = self.create_key()
        data = {
            "reg_key": "this is invalid",
            "key_type": args.get("key_type"),
            "gen_for": self.default_generated_for,
        }
        result = validate_registration_key(data)
        self.assertIn("error", result)

    def test_validate_registration_key_invalid_gen_for(self):
        args = self.create_key()
        data = {
            "reg_key": args.get("generated_key"),
            "key_type": args.get("key_type"),
            "gen_for": "Some Random Invalid Name",
        }
        result = validate_registration_key(data)
        self.assertIn("error", result)

    def test_save_account_id_valid(self):
        result = save_account_id(generate_account_id(0))
        self.assertEqual(
            result, AllAccountId.objects.values_list("generated_id", flat=True).first()
        )


class RegisterTests(APITestCase):
    # Each test with for loops must have their own email addresses to prevent
    # trigger of the unique email constraint, except when we are testing the
    # unique email constraint itself
    def setUp(self):
        self.url = reverse("register")
        self.default_data = {
            "last_name": "Potter",
            "first_name": "Harry",
            "email": "default_test_email@teest.com",
            "password": "1234",
            "address": "test address",
            "birthday": "1997-05-06",
            "phone": "+1800123456789",
        }
        self.default_generated_for = "Potter Harry"
        self.default_key_type = "STU"
        self.all_key_types = ["STU", "PAR", "EMP"]

    def generate_args(self, key_type=None, generated_for=None):
        url = reverse("reg_key")
        data = {
            "key_type": key_type or self.default_key_type,
            "generated_for": generated_for or self.default_generated_for,
        }
        return self.client.post(url, data, format="json")

    def create_dummy_student(self):
        args = self.generate_args()
        dict_args = {
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
        }
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        return StudentDetail.objects.values_list("account_id", flat=True).first()

    def test_valid_registration_minimum(self):
        test_emails = [
            "test_valid_registration_minimum_1@test.com",
            "test_valid_registration_minimum_2@test.com",
            "test_valid_registration_minimum_3@test.com",
        ]
        for key_type, email in list(zip(self.all_key_types, test_emails)):
            with self.subTest():
                args = self.generate_args(key_type)
                dict_args = {
                    "reg_key": args.data.get("generated_key"),
                    "key_type": args.data.get("key_type"),
                    "email": email,
                }
                data = self.default_data.copy()
                data.update(dict_args)
                if key_type == "PAR":
                    student = StudentDetail.objects.values_list(
                        "account_id", flat=True
                    ).first()
                    data.update({"relationship": "R", "student": student})
                elif key_type == "EMP":
                    data.update({"employment_type": "S"})
                response = self.client.post(self.url, data, format="json")
                self.assertEqual(response.data.get("success"), True)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_null_registration_args(self):
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_super_long_name(self):
        args = self.generate_args(
            generated_for="Dela Cruz Juan Karlos Miguel Marquez JR"
        )
        dict_args = {
            "last_name": "Dela Cruz",
            "first_name": "Juan Karlos",
            "middle_name": "Miguel Marquez",
            "suffix": "JR",
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
        }
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.data.get("success"), True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_phone_number(self):
        test_emails = [
            "test_missing_phone_number_1@test.com",
            "test_missing_phone_number_2@test.com",
            "test_missing_phone_number_3@test.com",
        ]
        for key_type, email in list(zip(self.all_key_types, test_emails)):
            with self.subTest():
                args = self.generate_args(key_type=key_type)
                dict_args = {
                    "email": email,
                    "reg_key": args.data.get("generated_key"),
                    "key_type": args.data.get("key_type"),
                }
                data = self.default_data.copy()
                data.pop("phone")
                data.update(dict_args)
                response = self.client.post(self.url, data, format="json")
                if key_type != "STU":
                    self.assertIn("error", response.data)
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                else:
                    self.assertEqual(response.data.get("success"), True)
                    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_address(self):
        args = self.generate_args()
        dict_args = {
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
        }
        data = self.default_data.copy()
        data.pop("address")
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_reg_key(self):
        args = self.generate_args()
        dict_args = {
            "key_type": args.data.get("key_type"),
        }
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_key_type(self):
        args = self.generate_args()
        dict_args = {"reg_key": args.data.get("generated_key")}
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_reg_key(self):
        args = self.generate_args()
        dict_args = {
            "reg_key": "this-key-is-invalid",
            "key_type": args.data.get("key_type"),
        }
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_key_type(self):
        args = self.generate_args()
        dict_args = {"reg_key": args.data.get("generated_key"), "key_type": "QQQ"}
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_suffix(self):
        args = self.generate_args(generated_for="Potter Harry XX")
        dict_args = {
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
            "suffix": "XX",
        }
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_emp_type(self):
        args = self.generate_args(key_type="EMP")
        dict_args = {
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
            "employment_type": "this is an invalid choice",
        }
        data = self.default_data.copy()
        data.update(dict_args)
        response = self.client.post(self.url, data, format="json")
        self.assertIn("error", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_taken_email(self):
        for attempt in range(2):
            args = self.generate_args()
            dict_args = {
                "reg_key": args.data.get("generated_key"),
                "key_type": args.data.get("key_type"),
            }
            data = self.default_data.copy()
            data.update(dict_args)
            response = self.client.post(self.url, data, format="json")
            if attempt + 1 == 2:
                self.assertIn("error", response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            else:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_age_validator(self):
        args = self.generate_args()
        invalid_birthdates = [date.today(), date.today() - relativedelta(years=10)]
        dict_args = {
            "reg_key": args.data.get("generated_key"),
            "key_type": args.data.get("key_type"),
        }
        for birthdate in invalid_birthdates:
            with self.subTest():
                dict_args_sub = dict_args.copy()
                dict_args_sub.update({"birthday": birthdate})
                data = self.default_data.copy()
                data.update(dict_args_sub)
                response = self.client.post(self.url, data, format="json")
                self.assertIn("error", response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest():
            valid_birthdate = date.today() - relativedelta(years=11)
            dict_args_sub = dict_args.copy()
            dict_args_sub.update({"birthday": valid_birthdate})
            data = self.default_data.copy()
            data.update(dict_args_sub)
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(response.data.get("success"), True)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_par_emp_age_validator(self):
        invalid_birthdates = [date.today(), date.today() - relativedelta(years=20)]
        test_key_types = ["PAR", "EMP"]
        args = [
            arg for arg in [self.generate_args(key_type=key) for key in test_key_types]
        ]
        dict_args = [
            {
                "reg_key": args[0].data.get("generated_key"),
                "key_type": args[0].data.get("key_type"),
                "email": "override_default_test_email_1@test.com",
                "relationship": "R",
                "student": self.create_dummy_student(),
            },
            {
                "reg_key": args[1].data.get("generated_key"),
                "key_type": args[1].data.get("key_type"),
                "email": "override_default_test_email_2@test.com",
                "employment_type": "S",
            },
        ]
        for test_case_args in dict_args:
            for birthdate in invalid_birthdates:
                with self.subTest():
                    subtest_args = test_case_args.copy()
                    subtest_args.update({"birthday": birthdate})
                    data = self.default_data.copy()
                    data.update(subtest_args)
                    response = self.client.post(self.url, data, format="json")
                    self.assertIn("error", response.data)
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            with self.subTest():
                valid_birthdate = date.today() - relativedelta(years=21)
                subtest_args = test_case_args.copy()
                subtest_args.update({"birthday": valid_birthdate})
                data = self.default_data.copy()
                data.update(subtest_args)
                response = self.client.post(self.url, data, format="json")
                self.assertEqual(response.data.get("success"), True)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)


if __name__ == "__main__":
    import django

    django.setup()
    APITestCase.run()
