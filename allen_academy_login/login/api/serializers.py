from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["account_type"] = user.account_type
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = self.user.email
        return data
