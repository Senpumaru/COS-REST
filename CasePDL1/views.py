from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.http import FileResponse
from CasePDL1.models import Case
from CasePDL1.serializers import (
    CaseCreateSerializer,
    CaseUpdateSerializer,
    CaseListSerializer,
)
from CasePDL1.filters import CaseFilter
from CasePDL1.PDF import Reporter
import io

### Case ###
## Create ##
# CBV #
class CaseDetail(APIView):
    """
    Create a case instance.
    """

    def post(self, request, format=None):

        data = request.data
        # Block numbers extraction
        blocks = data["block_number"]
        blocks = [d["blockNumber"] for d in blocks]

        slides = data["slide_number"]
        slides = [d["slideNumber"] for d in slides]

        case = {
            "date_of_registration": data["date_of_registration"],
            "personal_number": data["personal_number"],
            "institution": data["institution"],
            "block_number": blocks,
            "block_amount": data["block_amount"],
            "slide_number": slides,
            "slide_amount": data["slide_amount"],
            "diagnosis": data["diagnosis"],
            "doctor_sender": data["doctor_sender"],
        }
        serializer = CaseCreateSerializer(data=case, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## Update ##
class CaseUpdate(APIView):
    """
    Retrieve, update or delete a case instance.
    """

    def get(self, request, uuid, format=None):
        case = Case.objects.get(uuid=uuid)
        serializer = CaseUpdateSerializer(case)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        case = Case.objects.get(uuid=uuid)

        data = request.data
        # Block numbers extraction
        blocks = data["block_number"]
        blocks = [d["blockNumber"] for d in blocks]

        slides = data["slide_number"]
        slides = [d["slideNumber"] for d in slides]

        # Incorrect dates
        if data["date_of_registration"] > data["date_of_response"]:
            content = {
                "Date of response should not be earlier than date_of_registration"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = {
            # Registration Data
            "date_of_registration": data["date_of_registration"],
            "personal_number": data["personal_number"],
            "institution": data["institution"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "middle_name": data["middle_name"],
            "block_number": blocks,
            "block_amount": data["block_amount"],
            "slide_number": slides,
            "slide_amount": data["slide_amount"],
            "diagnosis": data["diagnosis"],
            "doctor_sender": data["doctor_sender"],
            # Case Data
            "date_of_response": data["date_of_response"],
            "doctor_sender": data["doctor_sender"],
            "micro_desc": data["micro_desc"],
            "case_conclusion": data["case_conclusion"],
            "clin_interpretation": data["clin_interpretation"],
        }

        serializer = CaseUpdateSerializer(case, data=data, many=False)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        case = Case.objects.get(uuid=uuid)
        case.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## List ##
# CBV
class CaseViewAPI(APIView):
    def get(self, request):
        cases = Case.objects.all()
        serializer = CaseListSerializer(cases, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CaseViewServer(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CaseFilter
    ordering_fields = [
        "date_of_registration",
        "personal_number",
        "block_number",
        "institution",
        "date_of_response",
    ]


## PDF ##
def case_pdf_report(request, uuid):

    case = Case.objects.get(uuid=uuid)
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    Reporter.Report(
        buffer=buffer,
        date_of_registration=case.date_of_registration,
        personal_number=case.personal_number,
        block_number=case.block_number,
        
        full_name=case.full_name,
        date_of_birth=case.date_of_birth,
        institution=case.institution,
        
        diagnosis=case.diagnosis,
        doctor_sender=case.doctor_sender,
        
        date_of_response=case.date_of_response,
        doctor_reporter=case.doctor_reporter,
        cancer_cell_percentage=case.cancer_cell_percentage,
        immune_cell_percentage=case.immune_cell_percentage,
        clin_interpretation=case.clin_interpretation
    )
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{case.personal_number}.pdf")