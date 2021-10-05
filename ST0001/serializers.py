from .models import Block, BlockGroup, Patient, Slide, SlideGroup
from rest_framework import serializers


class PatientSer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "uuid",
            "id_ambulatory",
            "last_name",
            "middle_name",
            "first_name",
            "country",
            "date_of_birth",
            "date_created",
        ]


class SlideGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideGroup
        fields = [
            "uuid",
            "patient",
            "block_group",
            "code",
        ]


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ["uuid", "patient", "block_group", "block", "slide_group", "code", "information"]


class BlockGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = [
            "uuid",
            "patient",
            "code",
            "information",
        ]


class BlockSerializer(serializers.ModelSerializer):
    patient = PatientSer(many=False, read_only=True)
    slides = SlideSerializer(source="Block_Slides", many=True, read_only=True)

    class Meta:
        model = Block
        fields = [
            "uuid",
            "orginization",
            "department",
            "organ",
            "patient",
            "block_group",
            "startCode",
            "count",
            "code",
            "slides",
            "information",
        ]


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "uuid",
            "id_ambulatory",
            "last_name",
            "middle_name",
            "first_name",
            "country",
            "date_of_birth",
        ]


class PatientDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    blocks = BlockSerializer(source="Patient_Blocks", many=True, read_only=True)
    slides = SlideSerializer(source="Patient_Slides", many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            "uuid",
            "full_name",
            "id_ambulatory",
            "orginization",
            "gender",
            "last_name",
            "middle_name",
            "first_name",
            "date_of_birth",
            "country",
            "city",
            "street",
            "home",
            "flat",
            "blocks",
            "slides",
            "date_created",
        ]
