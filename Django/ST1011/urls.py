from django.contrib import admin
from django.urls import path
from .views import CaseDetail, CaseUpdate, CaseViewAPI, CaseViewServer, case_pdf_report

urlpatterns = [
    ### Case ###
    ## CRUD ##
    path('cases/create/', CaseDetail.as_view(), name="Case-Create"),
    path('cases/<str:uuid>/update/', CaseUpdate.as_view(), name="Case-Update"),
    path('cases/<str:uuid>/pdf/', case_pdf_report, name="Case-Update"),
    path('cases/list/', CaseViewServer.as_view(), name="Cases-Backend"),
    path('cases/frontend/', CaseViewAPI.as_view(), name="Cases-Frontend"),
    
]