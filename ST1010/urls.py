from django.contrib import admin
from django.urls import path
from .views import (
    CaseAddendum,
    CaseCreate,
    CaseReview,
    CaseTransfer,
    ApprovalUpdate,
    CaseUpdate,
    CaseReview,
    CaseArchiveList,
    CaseListServer,
    ProfileConsultantList,
    ProfilePathologistList,
    ProfileView,
    UserCaseViewServer,
    CaseStatistics,
    case_pdf_report,
)

urlpatterns = [
    ### Permission ###
    path("permissions/<int:id>", ProfileView.as_view(), name="Profile-View"),
    path("pathologists", ProfilePathologistList.as_view(), name="Pathologists"),
    path("consultants", ProfileConsultantList.as_view(), name="Consultants"),
    ### Case ###
    ## CRUD ##
    path("cases/create/", CaseCreate.as_view(), name="Case-Create"),
    path("cases/<str:uuid>/transfer/", CaseTransfer.as_view(), name="Case-Transfer"),
    path("cases/<str:uuid>/update/", CaseUpdate.as_view(), name="Case-Update"),
    path("cases/<str:uuid>/review/", CaseReview.as_view(), name="Case-Review"),
    path("cases/<str:uuid>/addendum/", CaseAddendum.as_view(), name="Case-Addendum"),
    path("cases/<int:code>/<int:number>/archive/", CaseArchiveList.as_view(), name="Case-Archive"),
    path("cases/<str:uuid>/pdf/", case_pdf_report, name="Case-Update"),
    path("cases/list/", CaseListServer.as_view(), name="Cases-Backend"),
    path("user/cases/list/", UserCaseViewServer.as_view(), name="User-Cases-Backend"),
    path("cases/statistics/", CaseStatistics.as_view(), name="Cases-Statistics"),
    path("approval/<str:id>/update/", ApprovalUpdate.as_view(), name="Approval-Update"),
]
