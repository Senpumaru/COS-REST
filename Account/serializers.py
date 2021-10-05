from os import read

from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ST1010_Permission, ST1011_Permission, ServiceUser


class PermissionSerializerST1010(serializers.ModelSerializer):
    class Meta:
        model = ST1010_Permission
        fields = ["guest", "registrar", "consultant", "clinician", "pathologist"]


class PermissionSerializerST1011(serializers.ModelSerializer):
    class Meta:
        model = ST1011_Permission
        fields = ["guest", "registrar", "consultant", "clinician", "pathologist"]


class UserSerializer(serializers.ModelSerializer):
    ST1010_Permission = PermissionSerializerST1010(read_only=True, many=False)
    ST1011_Permission = PermissionSerializerST1011(read_only=True, many=False)

    class Meta:
        model = ServiceUser
        fields = ["id", "first_name", "middle_name", "last_name", "title", "signature", "ST1010_Permission", "ST1011_Permission"]


class UserSerializerWithToken(UserSerializer):
    # token = serializers.SerializerMethodField(read_only=True)
    application_rights = serializers.ReadOnlyField()

    class Meta:
        model = ServiceUser
        fields = [
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            # "token",
            "application_rights",
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
