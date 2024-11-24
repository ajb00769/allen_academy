from django.db import models
from edu_admin.models import ClassSchedule


class StudentCourse(models.Model):
    student_id = models.ForeignKey(
        "register.StudentDetail",
        to_field="account_id",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    course_id = models.ForeignKey(
        "edu_admin.Course",
        to_field="course_code",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )


class StudentSubjectBlock(models.Model):
    account_id = models.ForeignKey(
        "register.StudentDetail",
        to_field="account_id",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    schedule_id = models.ForeignKey(
        "edu_admin.ClassSchedule",
        to_field="schedule_id",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    def get_schedule_details(self):
        return ClassSchedule.objects.get(
            schedule_id=self.schedule_id.schedule_id,
            active_flag=True,
        )


class EmployeeSubjectBlock(models.Model):
    account_id = models.ForeignKey(
        "register.EmployeeDetail",
        to_field="account_id",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    schedule_id = models.ForeignKey(
        "edu_admin.ClassSchedule",
        to_field="schedule_id",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    def get_schedule_details(self):
        return ClassSchedule.objects.get(
            schedule_id=self.schedule_id.schedule_id,
            active_flag=True,
        )
