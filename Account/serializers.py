from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ServiceUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUser
        fields = [
            "id",
            "first_name",
            "last_name",
        ]
        depth = 1


class UserSerializerWithToken(UserSerializer):
    # token = serializers.SerializerMethodField(read_only=True)
    application_rights = serializers.ReadOnlyField()

    class Meta:
        model = ServiceUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            # "token",
            "application_rights",
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
