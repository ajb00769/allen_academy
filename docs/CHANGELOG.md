# CHANGELOG

## [0.1.1] - 2024-11-25
- **Fixed**: Bug where a student gets an invalid account type error when attempting to register caused by code attempting to store data into the wrong table.
- **Fixed**: Bug where updating a department returns the correct JSON response but no data is updated on the DB.
- **Fixed**: Bug where the wrong error message appears when a username/email is already taken.
- **Changed**: Registration logic to termiante the operation earlier in the code when username/email is already taken.
- **Fixed**: Bug where you can register an account without validating the year level or year teaching level of the teacher or the relationship of a parent and student.


## [0.1.0] - 2024-08-06
- **Fixed**: corrected logic of `create_department` in the enrollment API. It now records the `created_on` and `updated_on` fields correctly.
- **Updated**: Updated `TestingLogs.ods` to reflect the current tests done. More will be added to this document moving forward


## [0.0.5] - 2024-06-17

- **Added**: logic for handling banned users under `handle_jwt`, the framework already has a built-in handling for banned users from logging in


## [0.0.4] - 2024-06-16

- **Added**: unit tests for school_administration branch. Only able to add test for JWT checking, data validation and etc will be added in integration testing.
- school_administration fully working as of now. All manual tests passed.


## [0.0.3] - 2024-06-12

- **Added**: project folder for enrollment service
- **Added**: implemented school administration service where staff members with the appropriate access level can make changes to the right endpoints
- **Changed**: made minor changes to login/api/serializers.py and views.py to include the user account type in the JWToken in relation to the above
- **Removed**: `allow_login` field removed from register/models.py as it is redundant with the default `is_active` column already inherited from the default `AUTH_USER_MODEL`


## [0.0.2] - 2024-05-15

- **Added** created login service with JWT and it tested and working


## [0.0.1] - 2024-04-16

- **Added** initial functionality created for the register service