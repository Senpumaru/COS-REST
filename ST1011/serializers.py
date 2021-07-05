from rest_framework import serializers
from ST1011.models import Case
from ST1011.filters import CaseFilter

### Case ###
# Create #
class CaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "date_of_registration",
            "personal_number",
            "institution",
            "block_number",
            "block_amount",
            "slide_number",
            "slide_amount",
            "diagnosis",
            "doctor_sender"
        ]
        
# Update #
class CaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            ## Registration Data ##
            "uuid",
            "date_of_registration",
            "personal_number",
            "last_name",
            "first_name",
            "middle_name",
            "date_of_birth",
            "institution",
            "block_number",
            "block_amount",
            "slide_number",
            "slide_amount",
            "diagnosis",
            "doctor_sender",
            ## Report Data ##
            "date_of_response",
            "doctor_reporter",
            "cancer_cell_percentage",
            "immune_cell_percentage",
            "clin_interpretation",
        ]


# List #
class CaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "uuid",
            "date_of_registration",
            
            "personal_number",
            "institution",
            "block_number",
            
            "date_of_response",
            "clin_interpretation"
            
        ]
