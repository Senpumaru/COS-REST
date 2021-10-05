from .serializers import (
    BlockGroupSerializer,
    BlockSerializer,
    PatientCreateSerializer,
    PatientDetailsSerializer,
    PatientSer,
    SlideGroupSerializer,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Block, BlockGroup, Patient, Slide, SlideGroup
from rest_framework import filters, generics, pagination
import itertools

class PatientList(generics.ListAPIView):
    """
    List of Patients.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientDetailsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "id_ambulatory",
        "last_name",
        "middle_name",
        "first_name",
        "country",
        "Patient_Blocks__code",
        "Patient_Slides__code",
    ]


class PatientCreator(APIView):
    """
    Create and get single Patient.
    """

    def post(self, request, format=None):
        data = request.data
        serialized_data = {}

        ## Patient Data ##
        serialized_data.update({"id_ambulatory": data["ambulatoryNumber"]})
        serialized_data.update({"orginization": data["orginization"]})
        serialized_data.update({"gender": data["gender"]})
        serialized_data.update({"first_name": data["firstName"]})
        serialized_data.update({"middle_name": data["middleName"]})
        serialized_data.update({"last_name": data["lastName"]})
        serialized_data.update({"date_of_birth": data["dateBirth"]})
        # Address
        serialized_data.update({"country": data["country"]})
        serialized_data.update({"city": data["city"]})
        serialized_data.update({"street": data["street"]})
        serialized_data.update({"house": data["house"]})
        serialized_data.update({"flat": data["flat"]})

        serializer = PatientCreateSerializer(data=serialized_data)
        if serializer.is_valid():
            patient = serializer.save()

            ### Block Group Data ###
            if data["blockGroupCode"] != "":

                ## Block validation ##
                block_codes = []
                year_code = data["blockGroupYear"].split("-")[0]
                amount = data["blockGroupCount"]
                for number in range(int(amount) + 1):
                    block_code = str(int(data["blockGroupCode"]) + int(number)) + "/" + year_code
                    block_codes.append(block_code)
                block_check = Block.objects.filter(code__in=block_codes).exists()
                # Error
                if block_check:
                    return Response(
                        {"error": "Блоки уже присутствуют в базе данных. Регистрирован только пациент."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                    # Success
                else:
                    # Block Group Creation #
                    block_code_start = data["blockGroupCode"]
                    block_code_end = int(data["blockGroupCode"]) + int(amount)
                    block_group_code = str(block_code_start) + "-" + str(block_code_end) + "/" + year_code
                    block_group = BlockGroup.objects.create(
                        patient=patient,
                        department=data["blockGroupDepartment"],
                        organ=data["blockGroupOrgan"],
                        code=block_group_code,
                    )

                    # Slide Group Creation #
                    slide_group = SlideGroup.objects.create(
                        patient=patient, block_group=block_group, code=block_group_code
                    )

                    # Block & Slide Creation
                    for block_code in data["blockCodes"]:
                        block = Block.objects.create(
                            patient=patient,
                            block_group=block_group,
                            department=data["blockGroupDepartment"],
                            organ=data["blockGroupOrgan"],
                            code=block_code["block"],
                        )

                        slide = Slide.objects.create(
                            patient=patient,
                            block_group=block_group,
                            slide_group=slide_group,
                            code=block_code["block"],
                        )

                        slide.block.set([block])

            ### Block Data ###
            elif (data["blockGroupCode"] == "") and (len(data["blockCodes"]) >= 1):
                # Block & Slide Creation
                for block_code in data["blockCodes"]:
                    block_check = Block.objects.filter(code=block_code["code"]).exists()
                    # Error
                    if block_check:
                        return Response(
                            {"error": "Блоки уже присутствуют в базе данных. Регистрирован только пациент."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    # Success
                    block = Block.objects.create(
                        patient=patient,
                        department=block_code["department"],
                        code=block_code["code"],
                    )

            ### Slide Group Data ###
            if data["slideGroupCode"] != "":

                ## Slide validation ##
                slide_codes = []
                year_code = data["slideGroupYear"].split("-")[0]
                amount = data["slideGroupCount"]
                for slide_code in data["slideCodes"]:
                    slide_check = Slide.objects.filter(code=slide_code["slide"]).exists()
                    # Error
                    if slide_check:
                        return Response(
                            {"error": "МП уже присутствуют в базе данных. Регистрирован только пациент."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    # Success
                else:
                    # Slide Group Creation #
                    slide_code_start = data["slideGroupCode"]
                    slide_code_end = int(data["slideGroupCode"]) + int(amount)
                    slide_group_code = str(slide_code_start) + "-" + str(slide_code_end) + "/" + year_code
                    slide_group = SlideGroup.objects.create(
                        patient=patient,
                        department=data["slideDepartment"],
                        organ=data["slideOrgan"],
                        code=slide_group_code,
                    )

                    # Slide & Slide Creation
                    for slide_code in data["slideCodes"]:

                        slide = Slide.objects.create(
                            patient=patient,
                            slide_group=slide_group,
                            code=slide_code["slide"],
                        )

            ### Slide Data ###
            elif (data["slideGroupCode"] == "") and (len(data["slideCodes"]) >= 1):
                # Slide & Slide Creation
                for slide_code in data["slideCodes"]:
                    slide_check = Slide.objects.filter(code=slide_code["slide"]).exists()
                    # Error
                    if slide_check:
                        return Response(
                            {"error": "Блоки уже присутствуют в базе данных. Регистрирован только пациент."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    # Success
                    slide = Slide.objects.create(
                        patient=patient,
                        department=slide_code["department"],
                        organ=slide_code["organ"],
                        code=slide_code["slide"],
                    )

            return Response({"success": "Пациент успешно зарегестрирован."}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PatientDetail(APIView):
    """
    Retrieve, update or delete a Patient instance.
    """

    def get_object(self, uuid):
        try:
            return Patient.objects.get(uuid=uuid)
        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        patient = self.get_object(uuid)
        serializer = PatientDetailsSerializer(patient)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        print(uuid)
        patient = self.get_object(uuid)

        serializer = PatientDetailsSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Пациент успешно обновлен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        patient = self.get_object(uuid)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlockSlideList(generics.ListAPIView):
    """
    List of Blocks & Slides.
    """

    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "orginization",
        "code",
        "orginization",
        "department",
        "information",
    ]


class BlockCreator(APIView):
    """
    Create and get single BlockGroup.
    """

    def post(self, request, format=None):
        data = request.data
        ## Patient Data ##
        patient = Patient.objects.get(uuid=data["Patient UUID"])

        ### Block Data ###
        ## Block validation ##
        for block_data in data["blockCodes"]:

            block_check = Block.objects.filter(code=block_data["code"]).exists()
            # Error
            if block_check:
                return Response(
                    {"error": "Блоки уже присутствуют в базе данных."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Success
            else:
                # Block & Slide Creation
                for block_data in data["blockCodes"]:
                    block = Block.objects.create(
                        patient=patient,
                        startCode=str(block_data["startCode"]),
                        count=int(block_data["amount"]),
                        code=block_data["code"],
                    )

                    slide = Slide.objects.create(
                        patient=patient,
                        code=block_data["code"],
                    )

                    slide.block.set([block])

        return Response({"success": "Блоки успешно зарегестрированы."}, status=status.HTTP_201_CREATED)


class PatientHistory(generics.ListAPIView):
    """
    List of Patients.
    """

    queryset = Patient.objects.all().order_by('-date_created')[:10]
    serializer_class = PatientSer


class BlockDetail(APIView):
    """
    Retrieve, update or delete a Block instance.
    """

    def get_object(self, uuid):
        try:
            return Block.objects.get(uuid=uuid)
        except Block.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        patient = self.get_object(uuid)
        serializer = BlockSerializer(patient)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        print(uuid)
        patient = self.get_object(uuid)

        serializer = BlockSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        patient = self.get_object(uuid)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlideCreator(APIView):
    """
    Create and get single SlideGroup.
    """

    def post(self, request, format=None):
        data = request.data
        ## Patient Data ##
        patient = Patient.objects.get(uuid=data["Patient UUID"])

        ### Slide Data ###
        ## Slide validation ##
        for slide_data in data["slideCodes"]:

            slide_check = Slide.objects.filter(code=slide_data["code"]).exists()
            # Error
            if slide_check:
                return Response(
                    {"error": "МП уже присутствуют в базе данных."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Success
            else:
                # Slide & Slide Creation
                for slide_data in data["slideCodes"]:
                    slide = Slide.objects.create(
                        patient=patient,
                        code=slide_data["code"],
                    )

        return Response({"success": "МП успешно зарегестрированы."}, status=status.HTTP_201_CREATED)
