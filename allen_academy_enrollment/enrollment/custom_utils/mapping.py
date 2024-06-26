from register.custom_utils.constants import (
    EMPLOYEE_YEAR_LEVEL_CHOICES,
    PHD_CHOICES,
    MASTERS_CHOICES,
    LAW_CHOICES,
    COLLEGE_LEVEL_CHOICES,
    HIGH_SCHOOL_CHOICES,
    MIDDLE_SCHOOL_CHOICES,
    ELEMENTARY_SCHOOL_CHOICES,
)
from enrollment.models import StudentSubjectBlock, EmployeeSubjectBlock
from enrollment.api.serializers import (
    StudentSubjectBlockSerializer,
    EmployeeSubjectBlockSerializer,
)

teacher_student_yr_lvl_mapping = {
    EMPLOYEE_YEAR_LEVEL_CHOICES[1][0]: PHD_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES[2][0]: MASTERS_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES[3][0]: LAW_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES[4][0]: COLLEGE_LEVEL_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES[5][0]: HIGH_SCHOOL_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES[6][0]: MIDDLE_SCHOOL_CHOICES,
    EMPLOYEE_YEAR_LEVEL_CHOICES[7][0]: ELEMENTARY_SCHOOL_CHOICES,
}

enrollment_mapping = {
    "STU": {
        "model": StudentSubjectBlock,
        "serializer": StudentSubjectBlockSerializer,
    },
    "EMP": {
        "model": EmployeeSubjectBlock,
        "serializer": EmployeeSubjectBlockSerializer,
    },
}
