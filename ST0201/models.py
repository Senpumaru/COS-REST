import datetime
import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

### Treatment ###
class Treatment(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(
        verbose_name="ID",
        editable=False,
        primary_key=True,
        unique=True,
    )
    uuid = models.UUIDField(
        verbose_name="UUID",
        primary_key=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    patient = models.ForeignKey(
        to="Patient",
        on_delete=models.CASCADE,
        related_name="ST0201_Treatment_Patient",
        null=True,
        blank=False,
    )

    ICD10_CHOICES = [
        (
            "C18.0",
            "C18.0",
        ),
        (
            "C18.1",
            "C18.1",
        ),
        (
            "C18.2",
            "C18.2",
        ),
        (
            "C18.3",
            "C18.3",
        ),
        (
            "C18.4",
            "C18.4",
        ),
        (
            "C18.5",
            "C18.5",
        ),
        (
            "C18.5",
            "C18.5",
        ),
        (
            "C18.6",
            "C18.6",
        ),
        (
            "C18.7",
            "C18.7",
        ),
        (
            "C18.8",
            "C18.8",
        ),
        (
            "C18.9",
            "C18.9",
        ),
        (
            "C19",
            "C19",
        ),
        (
            "C20",
            "C20",
        ),
    ]

    icd10 = models.CharField(
        verbose_name="MKB X",
        choices=ICD10_CHOICES,
        max_length=300,
        null=True,
        blank=False,
    )

    date_of_diagnosis = models.DateField(
        verbose_name="Date of Diagnosis",
        null=True,
        blank=False,
    )

    treatment = models.BooleanField(
        verbose_name="Treatment - Performed",
        null=True,
        blank=False,
    )

    neo_adjuvant_radiotherapy = models.BooleanField(
        verbose_name="Neoadjuvant chemotherapy - Performed",
        null=True,
        blank=False,
    )

    neo_adjuvant_radiotherapy_type = models.CharField(
        verbose_name="Neoadjuvant chemotherapy - Type",
        max_length=800,
        null=True,
        blank=False,
    )

    neo_adjuvant_radiotherapy_type_other = models.CharField(
        verbose_name="Neoadjuvant chemotherapy - Type (Other)",
        max_length=800,
        null=True,
        blank=False,
    )

    date_of_neo_adjuvant_radiotherapy = models.DateField(
        null=True,
        blank=False,
    )

    surgery = models.BooleanField(
        verbose_name="Surgery - Performed",
        null=True,
        blank=False,
    )

    surgery_type = models.CharField(
        verbose_name="Surgery - Type",
        max_length=800,
        null=True,
        blank=False,
    )

    date_surgery = models.DateField(
        null=True,
        blank=False,
    )

    adjuvant_therapy = models.BooleanField(
        verbose_name="Adjuvant Therapy - Performed",
        null=True,
        blank=False,
    )

    class Meta:
        db_table = "Treatment"
        verbose_name_plural = "Treatments"


### Treatment - Adjuvant ###
class TreatAdjuvant(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(
        verbose_name="ID",
        editable=False,
        primary_key=True,
        unique=True,
    )
    uuid = models.UUIDField(
        verbose_name="UUID",
        primary_key=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )
    patient = models.ForeignKey(
        to="Patient",
        on_delete=models.CASCADE,
        related_name="ST0201_TreatAdjuvant_Patient",
        null=True,
        blank=False,
    )
    adjuvant_radiotherapy_type = models.CharField(
        verbose_name="Adjuvant therapy - Type",
        max_length=800,
        null=True,
        blank=False,
    )

    adjuvant_radiotherapy_type_other = models.CharField(
        verbose_name="Adjuvant therapy - Type (Other)",
        max_length=800,
        null=True,
        blank=False,
    )

    date_of_adjuvant_radiotherapy = models.DateField(
        null=True,
        blank=False,
    )


### Diagnosis ###
class Diagnosis(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(
        verbose_name="ID",
        editable=False,
        primary_key=True,
        unique=True,
    )
    uuid = models.UUIDField(
        verbose_name="UUID",
        primary_key=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    patient = models.ForeignKey(
        to="Patient",
        on_delete=models.CASCADE,
        related_name="ST0201_Diagnosis_Patient",
        null=True,
        blank=False,
    )

    pT_CHOICES = [
        ("X", "X"),
        ("is", "is"),
        ("0", "0"),
        ("1", "1"),
        ("1a", "1a"),
        ("1b", "1b"),
        ("2", "2"),
        ("2a", "2a"),
        ("2b", "2b"),
        ("3", "3"),
        ("3a", "3a"),
        ("3b", "3b"),
        ("4", "4"),
        ("4a", "4a"),
        ("4b", "4b"),
    ]

    pT = models.CharField(
        verbose_name="pT",
        max_length=5,
        choices=pT_CHOICES,
        default="0",
        null=True,
        blank=False,
    )

    pN_CHOICES = [
        ("X", "X"),
        ("0", "0"),
        ("1", "1"),
        ("1a", "1a"),
        ("1b", "1b"),
        ("2", "2"),
        ("2a", "2a"),
        ("2b", "2b"),
    ]

    pN = models.CharField(
        verbose_name="pN",
        max_length=5,
        choices=pN_CHOICES,
        default="0",
        null=True,
        blank=False,
    )

    pM_CHOICES = [
        ("0", "0"),
        ("1", "1"),
        ("1a", "1a"),
        ("1b", "1b"),
        ("1c", "1c"),
    ]

    pM = models.CharField(
        verbose_name="pM",
        max_length=5,
        choices=pM_CHOICES,
        default="0",
        null=True,
        blank=False,
    )

    R_CHOICES = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("X", "X"),
    ]

    R = models.CharField(
        verbose_name="R",
        max_length=5,
        choices=R_CHOICES,
        default="0",
        null=True,
        blank=False,
    )

    G_CHOICES = [
        ("Low Grade", "Low Grade"),
        ("High Grade", "High Grade"),
    ]

    G = models.CharField(
        verbose_name="G",
        max_length=15,
        choices=G_CHOICES,
        null=True,
        blank=False,
    )

    V_CHOICES = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("X", "X"),
    ]

    V = models.CharField(
        verbose_name="V",
        max_length=5,
        choices=V_CHOICES,
        default="0",
        null=True,
        blank=False,
    )

    L_CHOICES = [
        ("0", "0"),
        ("1", "1"),
        ("X", "X"),
    ]

    L = models.CharField(
        verbose_name="L",
        max_length=5,
        choices=L_CHOICES,
        default="0",
        null=True,
        blank=False,
    )

    date_of_progression = models.DateField(
        null=True,
        blank=False,
    )

    metastasis = models.CharField(
        verbose_name="Metastasis",
        max_length=200,
        null=True,
        blank=False,
    )
    metastasis_location = models.CharField(
        verbose_name="Metastasis Location",
        max_length=200,
        null=True,
        blank=False,
    )

    metastasis_location_other = models.CharField(
        verbose_name="Metastasis Location - Other",
        max_length=200,
        null=True,
        blank=False,
    )

    progression_commentary = models.CharField(
        verbose_name="Progression - Commentary",
        max_length=800,
        null=True,
        blank=False,
    )

    date_of_visit = models.DateField(
        null=True,
        blank=False,
    )

    date_of_death = models.DateField(
        null=True,
        blank=False,
    )
    status_type = models.IntegerChoices(
        verbose_name="",
        null=True,
        blank=False,
    )

    @property
    def pTNMRGVL(self):
        stage = (
            "pT" + self.pT + "pN" + self.pN + "pM" + self.pM + "R" + self.R + "G" + self.G + "V" + self.V + "L" + self.L
        )
        return stage

    @property
    def stage(self):
        deducsion = ""
        if self.pT == "1":
            deducsion = ("IIIA",)
        elif self.pT == "2":
            deducsion = ("IIIA",)
        elif self.pT == "3":
            deducsion = ("IIIA",)
        elif self.pT == "3":
            deducsion = ("IIIA",)
        return deducsion

    class Meta:
        db_table = "Diagnosis"
        verbose_name_plural = "Diagnoses"

### Morphology ###
class Morphology(models.Model):
    histological_type_who_2019 = models.CharField(
        verbose_name="Histological Type (WHO 2019)",
        max_length=100,
        null=True,
        blank=False,
    )
    adenocarcinoma_differentiation_level = models.CharField(
        verbose_name="Adenocarcinoma differentiation level",
        max_length=10,
        null=True,
        blank=False,
    )

    interepithelial_lymphocyte_presence = models.CharField(
        verbose_name="Interepithelial lymphocyte presence",
        max_length=10,
        null=True,
        blank=False,
    )
    nuclei_polarity  = models.CharField(
        verbose_name="Nuclei polarity",
        max_length=10,
        null=True,
        blank=False,
    )
    construction_type= models.CharField(
        verbose_name="Construction type",
        max_length=10,
        null=True,
        blank=False,
    )
    infiltration_edge = models.CharField(
        verbose_name="Infiltration Edge",
        max_length=10,
        null=True,
        blank=False,
    )

    pyogenic_inflammatory_reaction = models.CharField(
        verbose_name="Pyogenic reaction",
        max_length=10,
        null=True,
        blank=False,
    )

    stroma_maturity = models.CharField(
        verbose_name="Stroma maturity",
        max_length=10,
        null=True,
        blank=False,
    )

    stroma_type = models.CharField(
        verbose_name="Stroma type",
        max_length=10,
        null=True,
        blank=False,
    )

    localization = models.CharField(
        verbose_name="Stroma type",
        max_length=10,
        null=True,
        blank=False,
    )

    circular_growth = models.CharField(
        verbose_name="Circular growth (< 1 mm)",
        max_length=10,
        null=True,
        blank=False,
    )

    invasion_level = models.CharField(
        verbose_name="Circular growth (< 1 mm)",
        max_length=10,
        null=True,
        blank=False,
    )