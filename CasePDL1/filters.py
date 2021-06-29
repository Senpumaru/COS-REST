from django_filters import rest_framework
from rest_framework import generics
from CasePDL1.models import Case

class CaseFilter(rest_framework.FilterSet):
    date_of_registration_gte = rest_framework.DateFilter(field_name="date_of_registration", lookup_expr='gte')
    date_of_registration_lte = rest_framework.DateFilter(field_name="date_of_registration", lookup_expr='lte')
    
    personal_number = rest_framework.NumberFilter(field_name="personal_number", lookup_expr='contains')
    block_number = rest_framework.NumberFilter(field_name="block_amount", lookup_expr='icontains')
    institution = rest_framework.CharFilter(field_name="institution", lookup_expr='icontains')

    class Meta:
        model = Case
        fields = ["date_of_registration", "personal_number", "block_number", 'institution']