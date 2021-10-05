import datetime
from ST1010.tasks import celery_send_report
from ST1010.serializers import DeliverySerializer
import io

import pandas as pd

from django.db import connection

from Account.models import ST1011_Permission, ServiceUser
from Account.permissions import AccessST1011
from Account.serializers import PermissionSerializerST1011, UserSerializer
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, pagination, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ST1011.serializers import (
    CaseArchiveCreateSerializer,
    CaseArchiveListSerializer,
    CaseAddendumSerializer,
    CaseApprovalCreateSerializer,
    CaseDeclineSerializer,
    CaseEditorUpdateSerializer,
    CaseApprovalUpdateSerializer,
    CaseCreateSerializer,
    CaseDetailsSerializer,
    CaseTransferSerializer,
    CaseCreatorUpdateSerializer,
    CaseListSerializer,
    ProfileListSerializer,
)

from ST1011.filters import CaseFilter
from ST1011.models import Approval, Case
from ST1011.PDF import Reporter
from ST1011.permissions import Clinician, Consultant, Guest, Pathologist, Registrar


### Permission ###
class ProfileView(APIView):
    def get(self, request, id, format=None):
        try:
            permission = ST1011_Permission.objects.get(user=id)
            serializer_class = PermissionSerializerST1011(permission, many=False)
            return Response(serializer_class.data)
        except:
            return Response(
                {"detail": "You do not have permissions for this applications, contact staff to acquire credentials."}
            )


class ProfilePathologistList(generics.ListAPIView):
    queryset = ST1011_Permission.objects.filter(pathologist=True)
    serializer_class = ProfileListSerializer


class ProfileConsultantList(generics.ListAPIView):
    queryset = ST1011_Permission.objects.filter(consultant=True)
    serializer_class = ProfileListSerializer


### Case ###
## Create ##
# CBV #
class CaseCreate(APIView):
    """
    Create a new case instance.
    """

    permission_classes = [AccessST1011 & (Registrar | Clinician | Pathologist)]

    def post(self, request, format=None):
        data = request.data
        print(data)
        
        ### Insert data for serialization ###
        ## Registration Data ##

        
        
        data.update({"case_consultants": data["caseConsultants"]})
        # Custom Data #
        data.update({"version": 1.0})
        data.update({"version_state": "In-progress"})
        # Miscellaneous #
        data.update({"case_creator": request.user.id})

        serializer_case = CaseCreateSerializer(data=data, many=False)
        if serializer_case.is_valid():

            case = serializer_case.save()

            ## Create CASE APPROVAL objects ##
            if len(data["case_consultants"]) > 0:
                for case_consultant in data["case_consultants"]:
                    case_approval_data = {
                        "case": case.id,
                        "consultant": case_consultant,
                    }
                    serializer_approval = CaseApprovalCreateSerializer(
                        data=case_approval_data,
                        many=False,
                    )
                    if serializer_approval.is_valid():
                        serializer_approval.save()
                    else:
                        Response(
                            serializer_approval.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            else:
                # No case consultants specified
                pass

            return Response(serializer_case.data, status=status.HTTP_201_CREATED)
        else:
            for key_error in serializer_case.errors:
                if key_error == "non_field_errors":
                    return Response(
                        {"Detail": "Код организации и ID уже существуют!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(serializer_case.errors, status=status.HTTP_400_BAD_REQUEST)


## Transfer ##
class CaseTransfer(APIView):
    """
    Transfer a case instance.
    """

    permission_classes = [AccessST1011 & (Registrar)]

    def put(self, request, uuid, format=None):
        data = request.data

        case = Case.objects.get(uuid=data["uuid"])

        serialized_data = {"case_assistant": data["caseAssistant"]}
        serializer = CaseTransferSerializer(case, data=serialized_data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## Update ##
class CaseUpdate(APIView):
    """
    Retrieve, update or delete a case instance.
    """

    permission_classes = [AccessST1011]

    def get(self, request, uuid, format=None):
        case = Case.objects.get(uuid=uuid)
        serializer = CaseDetailsSerializer(case)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        data = request.data

        ## Object former state ##
        case_former = Case.objects.get(uuid=data["uuid"])
        ## Former consultants ##
        case_former_serializer = CaseDetailsSerializer(case_former)
        case_former_data = case_former_serializer.data

        former_consultants = case_former_data["case_consultants"]
        former_consultants_id = [user["id"] for user in former_consultants]

        ## Data Serialization
        serialized_data = {}

        ## Insert data for serialization ##
        # Registration Data
        serialized_data.update({"date_of_dispatch": data["dateDispatch"]})
        serialized_data.update({"date_of_acquisition": data["dateAcquisition"]})
        serialized_data.update({"institution": data["institution"]})
        serialized_data.update({"personal_number": data["personalNumber"]})
        serialized_data.update({"date_of_birth": data["dateBirth"]})
        serialized_data.update({"last_name": data["lastName"]})
        serialized_data.update({"middle_name": data["middleName"]})
        serialized_data.update({"first_name": data["firstName"]})
        serialized_data.update({"block_codes": data["blockCodes"]})
        serialized_data.update({"block_count": data["blockCount"]})
        serialized_data.update({"slide_codes": data["slideCodes"]}),
        serialized_data.update({"slide_count": data["slideCount"]})
        serialized_data.update({"diagnosis": data["diagnosis"]})
        serialized_data.update({"case_sender": data["caseSender"]})
        serialized_data.update({"case_editor": data["caseEditor"]})
        serialized_data.update({"case_consultants": data["caseConsultants"]})

        ## Check user credentials ##
        user_serializer = UserSerializer(request.user)
        user_data = user_serializer.data
        creator = False
        editor = False

        print(case_former_data)

        if case_former_data["case_editor"]:
            if user_data["id"] == case_former_data["case_editor"]["id"]:
                editor = True
            else:
                editor = False

        if case_former_data["case_creator"]:
            if user_data["id"] == case_former_data["case_creator"]["id"]:
                creator = True
            else:
                if case_former_data["case_assistant"]:
                    if user_data["id"] == case_former_data["case_assistant"]["id"]:
                        creator = True
                    else:
                        creator = False
        else:
            pass

        if creator == True and editor == False:
            case_updated_serializer = CaseCreatorUpdateSerializer(case_former, data=serialized_data, many=False)
        elif editor == True:
            serialized_data.update({"date_of_report": data["dateReport"].split("T")[0]})
            serialized_data.update({"cancer_cell_percentage": data["cancerCellPercentage"]})
            serialized_data.update({"immune_cell_percentage": data["immuneCellPercentage"]})
            serialized_data.update({"clinical_interpretation": data["clinicalInterpretation"]})
            case_updated_serializer = CaseEditorUpdateSerializer(case_former, data=serialized_data, many=False)
        else:
            return Response({"Detail": "Not permitted!"}, status=status.HTTP_400_BAD_REQUEST)

        ## Serializer Validation ##
        if case_updated_serializer.is_valid():
            case_updated = case_updated_serializer.save()
            print(former_consultants_id)
            ## Consultants approval instances - Update
            for id in serialized_data["case_consultants"]:
                if id not in former_consultants_id:
                    case_approval_data = {"case": case_former_data["id"], "consultant": id}
                    case_approval_serializer = CaseApprovalCreateSerializer(data=case_approval_data)
                    if case_approval_serializer.is_valid():
                        case_approval_serializer.save()
                    else:
                        return Response(case_approval_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # Reset Case Approval
                if id in former_consultants_id:
                    case_consultant_object = ServiceUser.objects.get(id=id)
                    case_approval_object = Approval.objects.get(case=case_updated, consultant=case_consultant_object)
                    case_approval_object.approval = ""
                    case_approval_object.text = ""
                    case_approval_object.save()

            # Delete old approvals
            for id in former_consultants_id:
                if id not in serialized_data["case_consultants"]:
                    case_consultant_object = ServiceUser.objects.get(id=id)
                    case_approval_object = Approval.objects.get(case=case_updated, consultant=case_consultant_object)
                    case_approval_object.delete()

            return Response(case_updated_serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(case_updated_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        case = Case.objects.get(uuid=uuid)
        case.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## Decline ##
class CaseDecline(APIView):
    def put(self, request, uuid, format=None):
        data = request.data
        print(data)

        ## Object former state ##
        case_former = Case.objects.get(uuid=uuid)
        ## Former consultants ##
        case_former_serializer = CaseDetailsSerializer(case_former)
        case_former_data = case_former_serializer.data

        former_consultants = case_former_data["case_consultants"]
        former_consultants_id = [user["id"] for user in former_consultants]

        ## Data Serialization
        serialized_data = {}

        ## Insert data for serialization ##
        # Registration Data
        serialized_data.update({"case_consultants": data["caseConsultants"]})
        serialized_data.update({"decline_status": True})
        serialized_data.update({"decline_reason": data["declineReason"]})
        serialized_data.update({"clinical_interpretation": "Отказ"})
        case_decline_serializer = CaseDeclineSerializer(case_former, data=serialized_data, many=False)

        ## Serializer Validation ##
        if case_decline_serializer.is_valid():
            case_updated = case_decline_serializer.save()
            
            ## Consultants approval instances - Update
            for id in serialized_data["case_consultants"]:
                if id not in former_consultants_id:
                    case_approval_data = {"case": case_former_data["id"], "consultant": id}
                    case_approval_serializer = CaseApprovalCreateSerializer(data=case_approval_data)
                    if case_approval_serializer.is_valid():
                        case_approval_serializer.save()
                    else:
                        return Response(case_approval_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # Reset Case Approval
                if id in former_consultants_id:
                    case_consultant_object = ServiceUser.objects.get(id=id)
                    case_approval_object = Approval.objects.get(case=case_updated, consultant=case_consultant_object)
                    case_approval_object.approval = ""
                    case_approval_object.text = ""
                    case_approval_object.save()

            # Delete old approvals
            for id in former_consultants_id:
                if id not in serialized_data["case_consultants"]:
                    case_consultant_object = ServiceUser.objects.get(id=id)
                    case_approval_object = Approval.objects.get(case=case_updated, consultant=case_consultant_object)
                    case_approval_object.delete()

            return Response(case_decline_serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(case_decline_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## Review ##
class CaseReview(APIView):
    permission_classes = [AccessST1011]

    def put(self, request, uuid, format=None):
        data = request.data

        ## Check user credentials ##
        user_serializer = UserSerializer(request.user)
        user_data = user_serializer.data

        case_review = Case.objects.get(uuid=data["uuid"])

        editor = False

        if user_data["id"] == case_review.case_editor.id:
            editor = True
        else:
            editor = False

        ## Case Review ##
        # Verify current CASE-REPORT
        if editor == True:
            case_review.version_state = "Verified"
            case_review.date_of_report = datetime.date.today()
            case_review.save()
            return Response("Case Reviewed", status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"Detail": "Not permitted!"}, status=status.HTTP_400_BAD_REQUEST)


## Addendum ##
class CaseAddendum(APIView):
    permission_classes = [AccessST1011]

    def put(self, request, uuid, format=None):
        case_origin = Case.objects.get(uuid=uuid)

        data = CaseDetailsSerializer(case_origin).data

        # Check USER credentials #
        user_serializer = UserSerializer(request.user)
        user_data = user_serializer.data
        if user_data["id"] == case_origin.case_editor.id:
            editor = True
        else:
            editor = False

        # CASE Addendum #
        if editor == True:
            case_origin.version_state = "Obsolete"
            case_origin.save()

            # Create CASE (new Version)
            former_consultants = data["case_consultants"]
            former_consultants_id = [user["id"] for user in former_consultants]

            data["case_creator"] = data["case_creator"]["id"]
            if data["case_assistant"]:
                data["case_assistant"] = data["case_assistant"]["id"]
            data["case_editor"] = data["case_editor"]["id"]
            data["case_consultants"] = former_consultants_id
            data["version"] = float(data["version"]) + 1
            data["version_state"] = "In-progress"

            case_new_version_serializer = CaseAddendumSerializer(data=data, many=False)
            if case_new_version_serializer.is_valid():
                case_new_version = case_new_version_serializer.save()

                # Refresh APPROVAL instances
                for consultant_id in former_consultants_id:
                    case_approval_data = {"case": case_new_version.id, "consultant": consultant_id}
                    case_approval_serializer = CaseApprovalCreateSerializer(data=case_approval_data)
                    if case_approval_serializer.is_valid():
                        case_approval_serializer.save()
                    else:
                        return Response(case_approval_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(case_new_version_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(case_new_version_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Detail": "Not permitted!"}, status=status.HTTP_400_BAD_REQUEST)


### Archive ###
class CaseArchiveList(generics.ListAPIView):
    # permission_classes = [AccessST1011]

    def get(self, request, personal_number, format=None):
        queryset = Case.objects.filter(~Q(version_state="In-progress"), personal_number=personal_number)
        serializer_class = CaseListSerializer(queryset, many=True)
        return Response(serializer_class.data)


## List ##
# Search #
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# CBV
class CaseListServer(generics.ListAPIView):
    permission_classes = [AccessST1011]
    queryset = Case.objects.filter(
        Q(version_state="In-progress") | Q(version_state="Verified") | Q(version_state="Declined")
    )
    serializer_class = CaseListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CaseFilter
    ordering_fields = [
        "date_of_acquisition",
        "institution",
        "date_of_response",
        "staining_pattern",
    ]
    ordering = ["-date_of_acquisition"]


class CaseViewAPI(APIView):
    permission_classes = [AccessST1011]

    def get(self, request):
        cases = Case.objects.all()
        serializer = CaseListSerializer(cases, many=True)
        return Response(serializer.data)


# User Case #
class UserCaseViewServer(APIView):
    permission_classes = [AccessST1011]
    serializer_class = CaseListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CaseFilter
    ordering_fields = [
        "date_of_acquisition",
        "institution",
        "date_of_response",
        "staining_pattern",
    ]
    ordering = ["date_of_acquisition"]

    def get(self, request):

        queryset = Case.objects.filter(user_creator=request.user)
        serializer = CaseListSerializer(queryset, many=True)

        return Response(serializer.data)


## Statistics ##
class CaseStatistics(APIView):
    """
    Statistics for cases.
    """

    permission_classes = [AccessST1011]

    def get(self, request, format=None):

        # Python code to convert into dictionary
        def Convert(tup, di):
            di = dict(tup)
            return di

        ### SQL queries ###
        cursor = connection.cursor()

        cases = Case.objects.all()
        cases_count = cases.count()

        cases_in_work = cases.filter(clinical_interpretation=None).count()

        ### Statistics ###
        ## All-Time
        ## Group by institution
        # SQL
        cursor.execute(
            """
            SELECT institution_code, clinical_interpretation, COUNT(institution_code) 
            FROM "ST1010 Case"
            GROUP BY institution_code, clinical_interpretation;
            """
        )
        result = cursor.fetchall()

        # Pandas
        df = pd.DataFrame(result, columns=["Code", "State", "Count"])
        df["State"] = df["State"].fillna(value="No answer")
        df = df.pivot(index="Code", columns="State", values="Count").fillna(0)

        # Statistics
        statistics = df.to_dict(orient="records")

        ## Current month
        ## Group by institution
        cursor.execute(
            """
            SELECT institution_code, clinical_interpretation, COUNT(institution_code) 
            FROM "ST1010 Case"
            WHERE date_of_registration >= date_trunc('month', CURRENT_DATE)
            GROUP BY institution_code, clinical_interpretation;
            """
        )
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=["Code", "State", "Count"])
        df = df.pivot(index="State", columns="Code", values="Count").fillna(0)
        statistics_current = df.to_dict("index")

        return Response(
            {
                "statistics": statistics,
                # "statistics_current": statistics_current,
                # "case_states": df.index.values,
                # Summary
                # "cases_count": cases_count,
                # "cases_transfer_required": cases_transfer_required,
                # "cases_in_work": cases_in_work,
            },
        )


## Delivery ##
class caseDelivery(APIView):
    def post(self, request, personal_number, format=None):
        # Case information
        case = Case.objects.get(personal_number=personal_number, version_state="Verified")
        case_serializer = CaseDetailsSerializer(instance=case)
        case_serializer_data = case_serializer.data

        # Head Consultant
        head_consultant = ServiceUser.objects.get(first_name="Nicholas", last_name="Yafremau")
        head_consultant_serializer_data = UserSerializer(instance=head_consultant).data

        # Serializer data
        data = request.data
        email_editor = data["editorEmail"]
        email_recipient = data["recipientEmail"]

        ## Delivery confirmation ##
        serializer = DeliverySerializer(
            data={
                "case": case.id,
                "email_recipient": email_recipient,
            }
        )
        if serializer.is_valid():
            serializer.save()

            # Celery Task
            celery_send_report.delay(
                email_editor, email_recipient, case_serializer_data, head_consultant_serializer_data
            )
            return Response({"success": "Sent"})
        return Response({"success": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


### Approval ###
## Update ##
# CBV #
class ApprovalUpdate(APIView):

    permission_classes = [AccessST1011]

    def put(self, request, id, format=None):
        data = request.data

        approval = Approval.objects.get(id=data["id"])

        serialized_data = {"approval": data["approvalChoice"]}
        serializer = CaseApprovalUpdateSerializer(approval, data=serialized_data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## PDF ##
def case_pdf_report(request, uuid):

    case = Case.objects.get(uuid=uuid)
    head_consultant = ServiceUser.objects.get(first_name="Nicholas", last_name="Yafremau")
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    Reporter.Report(
        buffer=buffer,
        # Registration Data
        date_of_dispatch=str(case.date_of_dispatch),
        personal_number=case.personal_number,
        block_codes=case.block_codes,
        date_of_birth=case.date_of_birth,
        full_name=case.full_name,
        institution=case.institution,
        diagnosis=case.diagnosis,
        case_sender=case.case_sender,
        # Report Data
        date_of_report=str(case.date_of_report),
        case_editor_first_name=case.case_editor.first_name,
        case_editor_middle_name=case.case_editor.middle_name,
        case_editor_last_name=case.case_editor.last_name,
        case_editor_title=case.case_editor.title,
        case_editor_signature=case.case_editor.signature.url,
        head_consultant_first_name=head_consultant.first_name,
        head_consultant_middle_name=head_consultant.middle_name,
        head_consultant_last_name=head_consultant.last_name,
        head_consultant_title=head_consultant.title,
        head_consultant_signature=head_consultant.signature.url,
        decline_reason=case.decline_reason,
        cancer_cell_percentage=case.cancer_cell_percentage,
        immune_cell_percentage=case.immune_cell_percentage,
        clinical_interpretation=case.clinical_interpretation,
    )
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{case.personal_number}.pdf")
