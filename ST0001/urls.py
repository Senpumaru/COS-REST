from django.contrib import admin
from django.urls import path, include
from .views import BlockCreator, BlockDetail, PatientHistory, BlockSlideList, PatientCreator, PatientDetail, PatientList, SlideCreator

urlpatterns = [
    ### Patient - Data ###
    path("patients/", PatientList.as_view(), name="Patient-List"),
    path("patient/history/", PatientHistory.as_view(), name="Patient-History"),
    path("patients/create/", PatientCreator.as_view(), name="Patient-Create"),
    path("patients/<str:uuid>/", PatientDetail.as_view(), name="Patient-Details"),
    path("patients/<str:uuid>/update/", PatientDetail.as_view(), name="Patient-Update"),
    # path("patients/delete/<int:pk>/", views.deletePatient, name="Patient-Delete"),
    ### BlockGroup - Data ###
    ## Blocks ##
    path("blocks/", BlockSlideList.as_view(), name="Block-List"),
    path("blocks/create/", BlockCreator.as_view(), name="Block-Create"),
    path("blocks/<str:uuid>/", BlockDetail.as_view(), name="Block-Details"),
    path("blocks/<str:uuid>/update/", BlockDetail.as_view(), name="Block-Update"),
    ### SlideGroup - Data ###
    ## Slides ##
    path("slides/create/", SlideCreator.as_view(), name="Slides-Create"),
]
