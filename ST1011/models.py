from django.db import models

# Create your models here.
import uuid
from Account.models import ServiceUser
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.postgres.fields import *
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class CaseArchive(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=False,
    )
    personal_number = models.CharField(
        unique=False,
        max_length=50,
        null=True,
        blank=False,
    )

    class Meta:
        db_table = "ST1011 Case Archive"
        verbose_name_plural = "ST1011 Case Archives"


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )
    archive = models.ForeignKey(
        to="CaseArchive",
        related_name="cases",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    ### Case Data ###
    ## Registration Data ##
    date_of_dispatch = models.DateField(
        default=datetime.date.today,
        null=True,
        blank=False,
    )
    date_of_acquisition = models.DateField(
        default=datetime.date.today,
        null=True,
        blank=False,
    )
    date_of_registration = models.DateField(
        default=datetime.date.today,
        null=True,
        blank=False,
    )
    personal_number = models.CharField(
        verbose_name="ID",
        default="Нет данных",
        unique=False,
        max_length=18,
        null=True,
        blank=True,
    )
    case_editor = models.ForeignKey(
        on_delete=models.CASCADE,
        to=ServiceUser,
        related_name="CaseEditorST1011",
        null=True,
        blank=True,
    )
    case_consultants = models.ManyToManyField(
        to=ServiceUser,
        related_name="CaseConsultantsST1011",
        default=[],
        blank=True,
    )
    patient = models.ForeignKey(
        to="Patient",
        on_delete=models.CASCADE,
        related_name="Patient_ST1011_Case",
        null=True,
        blank=True,
    )
    INSTITUTION_CHOICES = [
        (
            "Не указан",
            "Не указан",
        ),
        (
            "УЗ «Брестский областной онкологический диспансер»",
            "УЗ «Брестский областной онкологический диспансер»",
        ),
        (
            "УЗ «Гомельский областной клинический онкологический диспансер»",
            "УЗ «Гомельский областной клинический онкологический диспансер»",
        ),
        (
            "УЗ «Витебский областной клинический онкологический диспансер»",
            "УЗ «Витебский областной клинический онкологический диспансер»",
        ),
        (
            "УЗ «Могилёвский областной онкологический диспансер»",
            "УЗ «Могилёвский областной онкологический диспансер»",
        ),
        (
            "УЗ «Гродненский областной онкологический диспансер»",
            "УЗ «Гродненский областной онкологический диспансер»",
        ),
        (
            "УЗ «Минский городской клинический онкологический диспансер»",
            "УЗ «Минский городской клинический онкологический диспансер»",
        ),
        (
            "УЗ «Барановичский онкологический диспансер»",
            "УЗ «Барановичский онкологический диспансер»",
        ),
        (
            "УЗ «Бобруйский межрайонный онкологический диспансер»",
            "УЗ «Бобруйский межрайонный онкологический диспансер»",
        ),
        (
            "ГУ «РНПЦ онкологии и медицинской радиологии им. Н.Н. Александрова»",
            "ГУ «РНПЦ онкологии и медицинской радиологии им. Н.Н. Александрова»",
        ),
    ]
    institution = models.CharField(
        verbose_name="Region",
        default="Не указан",
        max_length=100,
        choices=INSTITUTION_CHOICES,
        null=True,
        blank=False,
    )

    DIAGNOSIS_CHOICES = [
        (
            "Рак легких: немелкоклеточный рак",
            "Рак легких: немелкоклеточный рак",
        ),
        (
            "Рак мочевого пузыря: (уротелиальная) карцинома",
            "Рак мочевого пузыря: (уротелиальная) карцинома",
        ),
    ]

    diagnosis = models.CharField(
        default="Не указан",
        max_length=200,
        verbose_name="Diagnosis",
        null=True,
        blank=True,
    )
    case_sender = models.CharField(
        verbose_name="Doctor (Sender)",
        default="Не указан",
        max_length=50,
        null=True,
        blank=True,
    )

    ### Report Data ###
    date_of_report = models.DateField(
        null=True,
        blank=True,
    )
    cancer_cell_percentage = models.DecimalField(
        verbose_name="Cancer Cells %",
        decimal_places=1,
        default=None,
        max_digits=3,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=True,
        blank=True,
    )
    CANCER_CELL_CHOICES = [
        (
            "<1%",
            "<1%",
        ),
        (
            ">1%",
            ">1%",
        ),
    ]
    cancer_cell_category = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=CANCER_CELL_CHOICES,
        verbose_name="Cancer Cells Category",
    )
    immune_cell_percentage = models.DecimalField(
        verbose_name="Immune Cells %",
        decimal_places=1,
        default=None,
        max_digits=3,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=True,
        blank=True,
    )
    IMMUNE_CELL_CHOICES = [
        (
            "<1%",
            "<1%",
        ),
        (
            ">1%",
            ">1%",
        ),
    ]
    immune_cell_category = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=IMMUNE_CELL_CHOICES,
        verbose_name="Immune Cells Category",
    )

    INTERPRETATION_CHOICES = [
        (
            "Нет заключения",
            "Нет заключения",
        ),
        (
            "Отказ",
            "Отказ",
        ),
        (
            # "Исследованный образец опухолевой ткани является PD-L1-позитивным",
            "PD-L1 позитивный",
            "PD-L1 позитивный",
        ),
        (
            # "Исследованный образец опухолевой ткани является PD-L1-негативным",
            "PD-L1 негативный",
            "PD-L1 негативный",
        ),
    ]
    clinical_interpretation = models.CharField(
        default="Нет заключения",
        max_length=200,
        null=True,
        blank=True,
        choices=INTERPRETATION_CHOICES,
        verbose_name="Clinical Interpratation",
    )
    
    decline_status = models.BooleanField(
        null=True,
        blank=True,
        default=False
    )

    DECLINE_CHOICES = [
        (
            "Несоответствие клиническим критериям",
            "Несоответствие клиническим критериям",
        ),
        (
            "Нерепрезентативный материал",
            "Нерепрезентативный материал",
        ),
        (
            "Материал старше 3 лет",
            "Материал старше 3 лет",
        ),
        (
            "EGFR+ (НМРЛ)",
            "EGFR+ (НМРЛ)",
        ),
        (
            "Повторное направление",
            "Повторное направление",
        ),
        (
            "Не предоставлен материал",
            "Не предоставлен материал",
        ),
    ]
    decline_reason = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default="",
        choices=DECLINE_CHOICES,
        verbose_name="Decline Reason",
    )
    ## Miscellaneous ##
    case_creator = models.ForeignKey(
        to=ServiceUser,
        on_delete=models.SET_NULL,
        related_name="ST1011_case_creator",
        null=True,
        blank=False,
    )
    case_assistant = models.ForeignKey(
        to=ServiceUser,
        on_delete=models.SET_NULL,
        related_name="ST1011_case_assistant",
        null=True,
        blank=True,
    )
    date_created = models.DateField(
        verbose_name="Date Created",
        default=datetime.date.today,
        null=True,
        blank=True,
    )
    date_updated = models.DateField(
        verbose_name="Date Updated",
        auto_now=True,
        null=True,
        blank=True,
    )
    version = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
    )
    VERSION_STATE_CHOICES = [
        ("In-progress", "In-progress"),
        ("Verified", "Verified"),
        ("Obsolete", "Obsolete"),
    ]
    version_state = models.CharField(
        choices=VERSION_STATE_CHOICES,
        max_length=20,
        null=True,
        blank=False,
    )

    @property
    def full_name(self):
        return str(self.last_name) + " " + str(self.first_name) + " " + str(self.middle_name) + " "

    def __str__(self) -> str:
        identifier = str(self.personal_number)
        return identifier

    class Meta:
        db_table = "ST1011 Case"
        verbose_name_plural = "ST1011 Cases"


class Delivery(models.Model):
    case = models.ForeignKey(
        to="Case",
        related_name="case_delivery",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    email_delivery = models.EmailField(
        null=True,
        blank=True,
    )
    date_of_delivery = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ST1011 Case Delivery"
        verbose_name_plural = "ST1011 Case Deliveries"


class Approval(models.Model):
    case = models.ForeignKey(
        to="Case",
        related_name="ST1011_case_approvals",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    consultant = models.ForeignKey(
        to=ServiceUser,
        related_name="ST1011_case_consultants",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    APPROVAL_CHOICE = ((True, "Yes"), (False, "No"))
    approval = models.BooleanField(
        choices=APPROVAL_CHOICE,
        null=True,
        blank=True,
    )
    text = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )

    ## Miscellaneous ##
    date_created = models.DateField(
        verbose_name="Date created",
        default=datetime.date.today,
        null=True,
        blank=True,
    )
    date_updated = models.DateField(
        verbose_name="Date updated",
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ST1011 Case Approval"
        verbose_name_plural = "ST1011 Case Approvals"
        unique_together = [["case", "consultant"]]
        ordering = ["date_created"]


class Comment(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )
    author = models.ForeignKey(
        to=ServiceUser,
        on_delete=models.CASCADE,
        related_name="ST1011_comment_author",
    )
    case = models.ForeignKey(
        to=Case,
        on_delete=models.CASCADE,
        related_name="comment_case",
    )
    content = models.TextField(
        max_length=200,
    )

    ## Miscellaneous ##
    date_created = models.DateField(
        verbose_name="Date Created",
        default=datetime.date.today,
        null=True,
        blank=True,
    )
    date_updated = models.DateField(
        verbose_name="Date Updated",
        auto_now=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.author) + ": " + str(self.content)[:20]

    def foo(self):
        return "stuff"

    class Meta:
        db_table = "ST1011 Comment"
        verbose_name_plural = "ST1011 Comments"
        ordering = ["date_created"]
