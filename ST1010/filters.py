from django_filters import rest_framework
from rest_framework import generics
from ST1010.models import Case


class CaseFilter(rest_framework.FilterSet):
    date_of_acquisition_gte = rest_framework.DateFilter(field_name="date_of_acquisition", lookup_expr="gte")
    date_of_acquisition_lte = rest_framework.DateFilter(field_name="date_of_acquisition", lookup_expr="lte")
    institution_code = rest_framework.NumberFilter(field_name="institution_code", lookup_expr="icontains")

    class Meta:
        model = Case
        fields = [
            "date_of_acquisition_gte",
            "date_of_acquisition_lte",
            "institution_code",
        ]
