from django_filters import rest_framework
from rest_framework import generics
from ST1010.models import Case, CaseArchive


class CaseFilter(rest_framework.FilterSet):
    date_of_registration_gte = rest_framework.DateFilter(field_name="date_of_registration", lookup_expr="gte")
    date_of_registration_lte = rest_framework.DateFilter(field_name="date_of_registration", lookup_expr="lte")
    institution_code = rest_framework.NumberFilter(field_name="institution_code", lookup_expr="icontains")

    class Meta:
        model = Case
        fields = [
            "date_of_registration_gte",
            "date_of_registration_lte",
            "institution_code",
        ]
