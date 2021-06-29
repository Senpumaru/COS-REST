import datetime
import uuid

from django.db.models.fields.related import ForeignKey

from Account.models import ServiceUser
from django.contrib.postgres.fields import *
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from model_utils import Choices


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=False,
    )

    ### Case Data ###
    ## Registration Data ##
    date_of_registration = models.DateField(
        default=datetime.date.today,
        null=True,
        blank=False,
    )
    INSTITUTION_CHOICES = [
        (000000, 000000),
        (328112, 328112),
        (328044, 328044),
        (328043, 328043),
        (327933, 327933),
        (327932, 327932),
    ]
    institution_code = models.PositiveIntegerField(
        verbose_name="Institution code",
        choices=INSTITUTION_CHOICES,
        null=True,
        blank=True,
    )
    order_number = models.PositiveIntegerField(
        unique=False,
        verbose_name="Order number",
        null=True,
        blank=False,
    )
    block_codes = ArrayField(
        models.CharField(max_length=20, null=True, blank=True),
        default=list,
        verbose_name="Block codes",
        null=True,
        blank=False,
    )
    block_count = models.PositiveIntegerField(
        verbose_name="Block count",
        default=1,
        null=True,
        blank=False,
    )
    slide_codes = ArrayField(
        base_field=models.CharField(max_length=20, null=True, blank=False),
        default=list,
        verbose_name="Slide codes",
        null=True,
        blank=True,
    )
    slide_count = models.PositiveIntegerField(
        verbose_name="Slide count",
        default=1,
        null=True,
        blank=True,
    )
    diagnosis = models.CharField(
        verbose_name="Diagnosis",
        max_length=500,
        null=True,
        blank=True,
    )
    case_sender = models.CharField(
        verbose_name="Case sender (Doctor)",
        max_length=50,
        null=True,
        blank=True,
    )
    case_editor = models.ForeignKey(
        on_delete=models.CASCADE,
        to=ServiceUser,
        related_name="CaseEditorST0001",
        null=True,
        blank=True,
    )
    case_consultants = models.ManyToManyField(
        to=ServiceUser,
        related_name="CaseConsultantsST0001",
        default=[],
        blank=True,
    )
    version = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
    )
    STATE_CHOICES = [(True, "In-production"), (False, "Reviewed")]
    version_state = models.BooleanField(
        choices=STATE_CHOICES,
        null=True,
        blank=False,
    )
    ## Report Data ##
    date_of_report = models.DateField(
        null=True,
        blank=True,
    )
    microscopic_description = models.TextField(
        verbose_name="Microscopic Description",
        max_length=1000,
        null=True,
        blank=True,
    )
    CASE_CHOICES = [
        (
            "Гранулярность не определяется",
            """Гранулярное цитоплазматическое окрашивание опухолевых клеток высокой интенсивности не определяется""",
        ),
        (
            "Окрашивание высокой интенсивности",
            """В большинстве опухолевых клеток определяется гранулярное цитоплазматическое окрашивание высокой интенсивности""",
        ),
    ]
    conclusion = models.CharField(
        verbose_name="Conclusion",
        choices=CASE_CHOICES,
        max_length=300,
        null=True,
        blank=True,
    )
    INTERPRETATION_CHOICES = [
        ("ALK-Positive", "ALK Позитивный"),
        ("ALK-Negative", "ALK Негативный"),
    ]
    clinical_interpretation = models.CharField(
        verbose_name="Clinical Interpretation",
        choices=INTERPRETATION_CHOICES,
        max_length=300,
        null=True,
        blank=True,
    )
    ## Miscellaneous ##
    case_creator = models.ForeignKey(
        to=ServiceUser,
        on_delete=models.SET_NULL,
        related_name="case_creator",
        null=True,
        blank=False,
    )
    case_assistant = models.ForeignKey(
        to=ServiceUser,
        on_delete=models.SET_NULL,
        related_name="case_assistant",
        null=True,
        blank=True,
    )
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

    @property
    def institution(self):
        INSTITUTION_CODES = {
            000000: "Не указан",
            328112: "УЗ «Гомельский областной клинический онкологический диспансер»",
            328044: "УЗ «Витебский областной клинический онкологический диспансер»",
            328043: "УЗ «Могилёвский областной онкологический диспансер»",
            327933: "УЗ «Минский городской клинический онкологический диспансер»",
            327932: "РНПЦ ОМР им. Н.Н. Александрова",
        }
        return INSTITUTION_CODES[self.institution_code]

    @property
    def case_code(self):
        property = str(self.institution_code) + "-" + str(self.order_number) 
        return property

    def __str__(self) -> str:
        return self.case_code + " Version: " + str(self.version)

    class Meta:
        db_table = "ST0001 Case"
        verbose_name_plural = "ST0001 Cases"
        unique_together = [["institution_code", "order_number", "version"]]
        ordering = ["date_of_registration"]


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
        db_table = "ST0001 Case Delivery"
        verbose_name_plural = "ST0001 Case Deliveries"
        

class Approval(models.Model):
    case = models.ForeignKey(
        to="Case",
        related_name="case_approvals",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    consultant = models.ForeignKey(
        to=ServiceUser,
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
        db_table = "ST0001 Case Approval"
        verbose_name_plural = "ST0001 Case Approvals"
        unique_together = [["case", "consultant"]]
        ordering = ["date_created"]


class Comment(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )
    author = models.ForeignKey(
        to=ServiceUser,
        on_delete=models.CASCADE,
        related_name="comment_author",
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
        db_table = "ST0001 Comment"
        verbose_name_plural = "ST0001 Comments"
        ordering = ["date_created"]
