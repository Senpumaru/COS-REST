from os import read
from django.contrib.postgres import fields
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ST1010.models import Approval, Case, CaseArchive
from Account.models import ST1010_Permission
from ST1010.filters import CaseFilter
from Account.serializers import UserSerializer

### Profile ###


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = ST1010_Permission
        fields = ["user", "guest", "registrar", "consultant", "clinician", "pathologist"]


### Case ###
# Create #
class CaseCreateSerializer(serializers.ModelSerializer):
    # archive = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    institution_code = serializers.CharField(required=True)
    order_number = serializers.IntegerField(required=True)
    case_sender = serializers.CharField(required=False, allow_null=True)
    block_codes = serializers.ListSerializer(child=serializers.CharField())
    slide_codes = serializers.ListSerializer(child=serializers.CharField())
    version = serializers.FloatField(required=True)

    class Meta:
        model = Case
        fields = [
            "archive",
            ## Registration Data ##
            "date_of_registration",
            "institution_code",
            "order_number",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            "version",
            "version_state",
            ## Miscellaneous ##
            "case_creator",
        ]
        validators = [
            UniqueTogetherValidator(queryset=Case.objects.all(), fields=["institution_code", "order_number", "version"])
        ]


# Addendum #
# Required for case duplication
class CaseAddendumSerializer(serializers.ModelSerializer):
    institution_code = serializers.CharField(required=True)
    order_number = serializers.IntegerField(required=True)
    case_sender = serializers.CharField(required=False, allow_null=True)
    block_codes = serializers.ListSerializer(child=serializers.CharField())
    slide_codes = serializers.ListSerializer(child=serializers.CharField())
    version = serializers.FloatField(required=True)

    class Meta:
        model = Case
        fields = [
            "archive",
            ## Registration Data ##
            "date_of_registration",
            "institution_code",
            "order_number",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            "version",
            "version_state",
            ## Report Data ##
            "date_of_report",
            "microscopic_description",
            "histological_description",
            "staining_pattern",
            "clinical_interpretation",
            ## Miscellaneous ##
            "case_creator",
            "case_assistant",
        ]
        validators = [
            UniqueTogetherValidator(queryset=Case.objects.all(), fields=["institution_code", "order_number", "version"])
        ]


# Update
class CaseApprovalUpdateSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    consultant = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    approval = serializers.BooleanField(required=True)
    text = serializers.CharField(required=False)

    class Meta:
        model = Approval
        fields = ["id", "case", "consultant", "approval", "text"]


# Details #
class CaseDetailsSerializer(serializers.ModelSerializer):
    case_editor = UserSerializer(read_only=True, many=False)
    case_consultants = UserSerializer(read_only=True, many=True)

    case_creator = UserSerializer(read_only=True, many=False)
    case_assistant = UserSerializer(read_only=True, many=False)
    case_approvals = CaseApprovalUpdateSerializer(read_only=True, many=True)

    institution = serializers.SerializerMethodField()
    case_code = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            "id",
            "uuid",
            ## Registration Data ##
            "date_of_registration",
            "institution_code",
            "order_number",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            "version",
            "version_state",
            ## Report Data ##
            "date_of_report",
            "microscopic_description",
            "histological_description",
            "staining_pattern",
            "clinical_interpretation",
            ## Approvals ##
            "case_approvals",
            ## Miscellaneous ##
            "case_creator",
            "case_assistant",
            ## Properties ##
            "institution",
            "case_code",
        ]

    def get_institution(self, obj):
        return obj.institution

    def get_case_code(self, obj):
        return obj.case_code


# Transfer #
class CaseTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ["case_assistant"]


# Update #
# Creator
class CaseCreatorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "uuid",
            ## Registration Data ##
            "date_of_registration",
            "institution_code",
            "order_number",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
        ]


# Editor
class CaseEditorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "uuid",
            ## Registration Data ##
            "date_of_registration",
            "institution_code",
            "order_number",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            ## Report Data ##
            "date_of_report",
            "microscopic_description",
            "histological_description",
            "staining_pattern",
            "clinical_interpretation",
        ]


### Approval ###
# Create #
class CaseApprovalCreateSerializer(serializers.ModelSerializer):
    approval = serializers.BooleanField(required=False)
    text = serializers.CharField(required=False)

    class Meta:
        model = Approval
        fields = ["case", "consultant", "approval", "text"]


### Case Archive ###
class CaseArchiveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseArchive
        fields = ["name"]


class CaseArchiveListSerializer(serializers.ModelSerializer):
    cases = CaseDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = CaseArchive
        fields = ["cases", "name"]


### Case & Approval ###
# List #
class CaseListSerializer(serializers.ModelSerializer):
    institution = serializers.SerializerMethodField()
    case_code = serializers.SerializerMethodField()

    case_editor = UserSerializer(read_only=True, many=False)
    case_consultants = UserSerializer(read_only=True, many=True)
    version = serializers.IntegerField()

    case_creator = UserSerializer(read_only=True, many=False)

    case_assistant = UserSerializer(read_only=True, many=False)
    case_approvals = CaseApprovalUpdateSerializer(read_only=True, many=True)

    class Meta:
        model = Case
        fields = [
            ## Registration Data ##
            "uuid",
            "date_of_registration",
            "institution_code",
            "order_number",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            "version",
            "version_state",
            ## Report Data ##
            "date_of_report",
            "microscopic_description",
            "histological_description",
            "staining_pattern",
            "clinical_interpretation",
            ## Approvals ##
            "case_approvals",
            ## Miscellaneous ##
            "case_creator",
            "case_assistant",
            ## Properties ##
            "institution",
            "case_code",
        ]

    def get_institution(self, obj):
        return obj.institution

    def get_case_code(self, obj):
        return obj.case_code
