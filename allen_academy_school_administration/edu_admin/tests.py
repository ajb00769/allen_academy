from django.urls import reverse

# from django.core.exceptions import ValidationError
# from datetime import date, time
from rest_framework import status
from rest_framework.test import APITestCase


class JWTHandlingTest(APITestCase):
    def test_create_department(self):
        self.url = reverse("create_dept")
        payload = {
            "dept_id": "ENGG",
            "dept_name": "Engineering Department",
            "dept_head": "202400000",
            "created_by": "202400000",
            "created_on": "2024-06-14",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)

    def test_create_course(self):
        self.url = reverse("create_course")
        payload = {
            "dept_id": "ENGG",
            "total_units": 127,
            "course_name": "Electrical Engineering",
            "course_code": "BSEE",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)

    def test_create_subject(self):
        self.url = reverse("create_subject")
        payload = {
            "subject_code": "DC",
            "subject_type": "M",
            "subject_name": "Differential Calculus",
            "subject_units": 4,
            "wk_class_dura": 1,
            "subject_tuition": 1904.21,
            "course_code": "BSME",
            "course_yr_lvl": "COL1",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)

    def test_create_subject_block(self):
        self.url = reverse("create_subject_block")
        payload = {
            "class_id": "1234",
            "subject_code": "DC",
            "subject_block": "MEA",
            "professor": "202400000",
            "semester": 1,
            "start_date": "2024-06-28",
            "end_date": "2024-09-11",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)

    def test_create_schedule(self):
        self.url = reverse("create_schedule")
        payload = {
            "schedule_id": 123,
            "class_id": "1234",
            "day_of_wk": "Tue",
            "start_time": "10:30",
            "end_time": "12:30",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)
