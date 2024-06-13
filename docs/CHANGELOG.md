# CHANGELOG


## [0.0.3] - 2024-06-12

- created project folder for enrollment service
- implemented school administration service where staff members with the appropriate access level can make changes to the right endpoints
- made minor changes to login/api/serializers.py and views.py to include the user account type in the JWToken in relation to the above
- **Removed**: `allow_login` field removed from register/models.py as it is redundant with the default `is_active` column already inherited from the default `AUTH_USER_MODEL`

## [0.0.2] - 2024-05-15

- created login service with JWT and it tested and working

## [0.0.1] - 2024-04-16

- initial functionality created for the register service
- need to add access levels for staff accounts
- staff account requesting a registration key to be generated should be check if they have the appropriate level of access or authority to do so