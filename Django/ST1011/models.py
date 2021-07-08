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


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    ### Case Data ###
    ## Registration Data ##
    date_of_registration = models.DateField(
        default=now,
        null=True,
        blank=False,
    )
    personal_number = models.CharField(
        verbose_name="ID",
        default="Нет данных",
        unique=True,
        max_length=10,
        null=True,
        blank=True,
    )

    block_number = ArrayField(
        models.CharField(default="00000/00", max_length=20, blank=True),
        default=list,
        verbose_name="Block №",
        help_text="Пример заполнения: 00001/00, 00002/00",
        validators=[],
        null=True,
        blank=False,
    )
    block_amount = models.PositiveIntegerField(
        verbose_name="Blocks",
        default=1,
        null=True,
        blank=False,
    )
    slide_number = ArrayField(
        base_field=models.CharField(default="00000/00", max_length=20, blank=False),
        default=list,
        verbose_name="Slide №",
        help_text="Пример заполнения: 00001/00, 00002/00",
        validators=[],
        null=True,
        blank=False,
    )
    slide_amount = models.PositiveIntegerField(
        verbose_name="Slides",
        default=1,
        null=True,
        blank=False,
    )
    last_name = models.CharField(
        default="Doe",
        unique=False,
        max_length=20,
        verbose_name="Last Name",
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        default="John",
        unique=False,
        max_length=15,
        verbose_name="First Name",
        null=True,
        blank=True,
    )
    middle_name = models.CharField(
        default="Jenks",
        unique=False,
        max_length=15,
        verbose_name="Middle Name",
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
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
    ]
    institution = models.CharField(
        verbose_name="Region",
        default="Не указан",
        max_length=100,
        choices=INSTITUTION_CHOICES,
        null=True,
        blank=False,
    )

    diagnosis = models.CharField(
        default="Не указан",
        max_length=200,
        verbose_name="Diagnosis",
        null=True,
        blank=True,
    )
    doctor_sender = models.CharField(
        verbose_name="Doctor (Sender)",
        default="Не указан",
        max_length=50,
        null=True,
        blank=True,
    )

    ### Form Data ###
    date_of_response = models.DateField(
        null=True,
        blank=True,
    )
    DOCTOR_REPORT_CHOICE = [
        (
            "Не указан",
            "Не указан",
        ),
        (
            "Давыдов Д.А.",
            "Давыдов Д.А.",
        ),
        (
            "Киселев П.Г.",
            "Киселев П.Г.",
        ),
    ]
    doctor_reporter = models.CharField(
        verbose_name="Doctor (Reporter)",
        default="Не указан",
        max_length=20,
        choices=DOCTOR_REPORT_CHOICE,
        null=True,
        blank=True,
    )
    cancer_cell_percentage = models.DecimalField(
        verbose_name="Cancer Cells",
        decimal_places=1,
        max_digits=3,
        default=None,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=True,
        blank=True,
    )
    immune_cell_percentage = models.PositiveIntegerField(
        verbose_name="Immune Cells",
        default=1,
        null=True,
        blank=False,
    )

    INTERPRETATION_CHOICES = [
        (
            "Нет заключения",
            "Нет заключения",
        ),
        (
            # "Исследованный образец опухолевой ткани является PD-L1-позитивным",
            "PD-L1 positive",
            "PD-L1 позитивный",
        ),
        (
            # "Исследованный образец опухолевой ткани является PD-L1-негативным",
            "PD-L1 negative",
            "PD-L1 негативный",
        ),
    ]
    clin_interpretation = models.CharField(
        default="Нет заключения",
        max_length=200,
        null=True,
        blank=True,
        choices=INTERPRETATION_CHOICES,
        verbose_name="Clinical Interpratation",
    )
    decline_status = models.BooleanField(
        default=False,
        null=True,
        blank=False,
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
        choices=DECLINE_CHOICES,
        verbose_name="Clinical Interpratation",
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

    @property
    def full_name(self):
        return (
            str(self.last_name)
            + " "
            + str(self.first_name)
            + " "
            + str(self.middle_name)
            + " "
        )

    def __str__(self) -> str:
        identifier = str(self.personal_number)
        return identifier

    class Meta:
        db_table = "ST1011 Case"
        verbose_name_plural = "ST1011 Cases"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(
        to=ServiceUser, on_delete=models.CASCADE, related_name="AuthorsST1011"
    )
    case = models.ForeignKey(to=Case, on_delete=models.CASCADE, related_name="Comments")

    content = models.TextField()

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

    class Meta:
        db_table = "ST1011 Comment"
        verbose_name_plural = "ST1011 Comments"
        ordering = ["date_updated"]
