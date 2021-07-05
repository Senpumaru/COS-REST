from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from ST1010.models import Approval, Case
from ST1010.filters import CaseFilter
from Account.serializers import UserSerializer

### Case ###
# Create #
class CaseCreateSerializer(serializers.ModelSerializer):
    institution_code = serializers.CharField(required=True)
    order_number = serializers.IntegerField(required=True)
    case_sender = serializers.CharField(required=False, allow_null=True)
    block_codes = serializers.ListSerializer(child=serializers.CharField())
    slide_codes = serializers.ListSerializer(child=serializers.CharField())
    version = serializers.FloatField(required=True)

    class Meta:
        model = Case
        fields = [
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

# Create #
class CaseReviewSerializer(serializers.ModelSerializer):
    institution_code = serializers.CharField(required=True)
    order_number = serializers.IntegerField(required=True)
    case_sender = serializers.CharField(required=False, allow_null=True)
    block_codes = serializers.ListSerializer(child=serializers.CharField())
    slide_codes = serializers.ListSerializer(child=serializers.CharField())
    version = serializers.FloatField(required=True)

    class Meta:
        model = Case
        fields = [
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