from Account.models import ST1011_Permission
from Account.serializers import UserSerializer
from rest_framework import serializers
from ST1011.models import Approval, Case, CaseArchive, Delivery
from ST1011.filters import CaseFilter
from rest_framework.validators import UniqueTogetherValidator

### Profile ###


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = ST1011_Permission
        fields = ["user", "guest", "registrar", "consultant", "clinician", "pathologist"]


### Case ###
# Create #
class CaseCreateSerializer(serializers.ModelSerializer):
    institution = serializers.CharField(required=True)
    personal_number = serializers.CharField(required=True)
    case_sender = serializers.CharField(required=False, allow_null=True)
    block_codes = serializers.ListSerializer(child=serializers.CharField(required=False))
    slide_codes = serializers.ListSerializer(child=serializers.CharField(required=False))
    version = serializers.FloatField(required=True)

    class Meta:
        model = Case
        fields = [
            "archive",
            ## Registration Data ##
            "date_of_dispatch",
            "date_of_acquisition",
            "institution",
            "personal_number",
            "date_of_birth",
            "last_name",
            "middle_name",
            "first_name",
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
        validators = []


# Addendum #
# Required for case duplication
class CaseAddendumSerializer(serializers.ModelSerializer):
    institution = serializers.CharField(required=True)

    case_sender = serializers.CharField(required=False, allow_null=True)
    block_codes = serializers.ListSerializer(child=serializers.CharField())
    slide_codes = serializers.ListSerializer(child=serializers.CharField())
    version = serializers.FloatField(required=True)

    class Meta:
        model = Case
        fields = [
            "archive",
            ## Registration Data ##
            "date_of_dispatch",
            "date_of_acquisition",
            "institution",
            "personal_number",
            "date_of_birth",
            "last_name",
            "middle_name",
            "first_name",
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
        validators = []

# Decline
class CaseDeclineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Case
        fields = ["case_consultants", "decline_status", "decline_reason", "clinical_interpretation"]

## Approval ##
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
    case_approvals = CaseApprovalUpdateSerializer(source="ST1011_case_approvals", read_only=True, many=True)

    class Meta:
        model = Case
        fields = [
            "id",
            "uuid",
            ## Registration Data ##
            "date_of_dispatch",
            "date_of_acquisition",
            "institution",
            "personal_number",
            "date_of_birth",
            "last_name",
            "middle_name",
            "first_name",
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
            "cancer_cell_percentage",
            "immune_cell_percentage",
            "clinical_interpretation",
            "decline_status",
            "decline_reason",
            ## Approvals ##
            "case_approvals",
            ## Miscellaneous ##
            "case_creator",
            "case_assistant",
        ]


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
            "date_of_dispatch",
            "date_of_acquisition",
            "institution",
            "personal_number",
            "date_of_birth",
            "last_name",
            "middle_name",
            "first_name",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            ## Report Data ##
            "decline_reason",
        ]


# Editor
class CaseEditorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "uuid",
            ## Registration Data ##
            "date_of_dispatch",
            "date_of_acquisition",
            "institution",
            "personal_number",
            "date_of_birth",
            "last_name",
            "middle_name",
            "first_name",
            "block_codes",
            "block_count",
            "slide_codes",
            "slide_count",
            "diagnosis",
            "case_sender",
            "case_editor",
            "case_consultants",
            ## Report Data ##
            "decline_reason",
            "date_of_report",
            "cancer_cell_percentage",
            "immune_cell_percentage",
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


### Delivery ###
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["id","case", "email_recipient", "date_of_delivery"]

### Case Archive ###
class CaseArchiveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseArchive
        fields = ["personal_number"]


class CaseArchiveListSerializer(serializers.ModelSerializer):
    cases = CaseDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = CaseArchive
        fields = ["cases", "personal_number"]


### Case & Approval ###
# List #
class CaseListSerializer(serializers.ModelSerializer):
    case_editor = UserSerializer(read_only=True, many=False)
    case_consultants = UserSerializer(read_only=True, many=True)
    version = serializers.IntegerField()

    case_creator = UserSerializer(read_only=True, many=False)
    case_assistant = UserSerializer(read_only=True, many=False)
    case_approvals = CaseApprovalUpdateSerializer(source="ST1011_case_approvals", read_only=True, many=True)

    class Meta:
        model = Case
        fields = [
            "uuid",
            ## Registration Data ##
            "date_of_dispatch",
            "date_of_acquisition",
            "institution",
            "personal_number",
            "date_of_birth",
            "last_name",
            "middle_name",
            "first_name",
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
            "decline_status", 
            "decline_reason",
            "date_of_report",
            "cancer_cell_percentage",
            "immune_cell_percentage",
            "clinical_interpretation",
            ## Approvals ##
            "case_approvals",
            ## Miscellaneous ##
            "case_creator",
            "case_assistant",
        ]

    def get_institution(self, obj):
        return obj.institution

    def get_case_code(self, obj):
        return obj.case_code
