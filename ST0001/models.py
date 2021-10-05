import datetime
import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


### Patient Data ###
class Patient(models.Model):
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

    id_ambulatory = models.CharField(
        verbose_name="Ambulatory ID",
        unique=True,
        max_length=20,
        null=True,
        blank=False,
        error_messages={"unique": "Амбуляторный ID уже существует!"},
    )

    orginization = models.CharField(
        verbose_name="Orginization",
        max_length=100,
        null=True,
        blank=False,
    )
    department = models.CharField(
        verbose_name="Department",
        max_length=100,
        null=True,
        blank=False,
    )
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_CHOICES,
        max_length=20,
        null=True,
        blank=False,
    )

    last_name = models.CharField(
        verbose_name="Last name",
        unique=False,
        max_length=20,
        null=True,
        blank=False,
    )

    middle_name = models.CharField(
        verbose_name="Middle name",
        unique=False,
        max_length=20,
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        verbose_name="First name",
        unique=False,
        max_length=20,
        null=True,
        blank=False,
    )
    # Address
    country = models.CharField(
        verbose_name="Country",
        default="Not Defined",
        unique=False,
        max_length=300,
        null=True,
        blank=True,
    )
    city = models.CharField(
        verbose_name="City",
        default="Not Defined",
        unique=False,
        max_length=300,
        null=True,
        blank=True,
    )
    street = models.CharField(
        verbose_name="Street",
        default="Not Defined",
        unique=False,
        max_length=300,
        null=True,
        blank=True,
    )
    home = models.CharField(
        verbose_name="Home",
        default="Not Defined",
        unique=False,
        max_length=300,
        null=True,
        blank=True,
    )
    flat = models.CharField(
        verbose_name="Flat",
        default="Not Defined",
        unique=False,
        max_length=300,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        null=True,
        blank=True,
    )
    date_of_death = models.DateField(
        verbose_name="Date of Death",
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

    class Meta:
        db_table = "Patient"
        verbose_name_plural = "Patients"

    @property
    def full_name(self):
        identifier = " ".join([self.last_name, self.first_name,  self.middle_name])
        return identifier

    def __str__(self) -> str:
        identifier = " ".join([self.first_name, self.last_name, "(" + self.id_ambulatory + ")"])
        return identifier


### Block Data ###
class BlockGroup(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(
        verbose_name="ID",
        editable=False,
        primary_key=True,
        unique=True,
    )
    uuid = models.UUIDField(
        primary_key=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=False,
    )

    patient = models.ForeignKey(
        to="Patient",
        related_name="BlockGroup_Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
        null=True,
        blank=False,
    )
    department = models.CharField(
        verbose_name="Department",
        max_length=50,
        null=True,
        blank=True,
    )
    organ = models.CharField(
        verbose_name="Organ",
        max_length=50,
        null=True,
        blank=True,
    )

    code = models.CharField(
        verbose_name="Block Group",
        unique=True,
        max_length=20,
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

    class Meta:
        db_table = "Block Group"
        verbose_name_plural = "Block Groups"

    def __str__(self) -> str:
        identifier = str(self.code)
        return identifier


class Block(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(
        verbose_name="ID",
        editable=False,
        primary_key=True,
        unique=True,
    )
    uuid = models.UUIDField(
        primary_key=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=False,
    )
    orginization = models.CharField(
        verbose_name="Orginization",
        default="Not Defined",
        max_length=100,
        null=True,
        blank=False,
    )
    department = models.CharField(
        verbose_name="Department",
        default="Not Defined",
        max_length=50,
        null=True,
        blank=True,
    )
    organ = models.CharField(
        verbose_name="Organ",
        default="Not Defined",
        max_length=50,
        null=True,
        blank=True,
    )
    block_group = models.ForeignKey(
        to="BlockGroup",
        related_name="BlockGroup_Block",
        on_delete=models.CASCADE,
        verbose_name="Block Group",
        max_length=20,
        null=True,
        blank=False,
    )

    patient = models.ForeignKey(
        to=Patient,
        on_delete=models.CASCADE,
        related_name="Patient_Blocks",
        verbose_name="Ambulatory ID",
        null=True,
        blank=True,
    )
    startCode = models.CharField(
        verbose_name="Block Code Start",
        unique=True,
        max_length=20,
        null=True,
        blank=True,
    )
    count = models.IntegerField(
        verbose_name="Block Count",
        null=True,
        blank=True,
    )
    code = models.CharField(
        verbose_name="Block Code",
        
        unique=True,
        max_length=20,
        null=True,
        blank=True,
    )

    information = models.CharField(
        verbose_name="Information",
        max_length=200,
        unique=True,
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

    def __str__(self) -> str:
        identifier = str(self.code)
        return identifier

    @property
    def parts(self):
        codes = []
        for i in range(int(self.count)):
            code_line = int(self.startCode) + i
            codes.append(code_line)
        return codes

    class Meta:
        db_table = "Block"
        verbose_name_plural = "Blocks"


### Slide Data ###
class SlideGroup(models.Model):
    objects = models.Manager()

    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    block_group = models.ForeignKey(
        to="BlockGroup",
        on_delete=models.CASCADE,
        verbose_name="Block Group",
        max_length=20,
        null=True,
        blank=True,
    )

    patient = models.ForeignKey(
        to="Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
        null=True,
        blank=False,
    )
    orginization = models.CharField(
        verbose_name="Orginization",
        max_length=100,
        null=True,
        blank=False,
    )
    department = models.CharField(
        verbose_name="Department",
        max_length=50,
        null=True,
        blank=True,
    )
    organ = models.CharField(
        verbose_name="Organ",
        max_length=50,
        null=True,
        blank=True,
    )
    code = models.CharField(
        verbose_name="Slide Group",
        unique=True,
        max_length=20,
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

    def __str__(self) -> str:
        identifier = str(self.code)
        return identifier

    class Meta:
        db_table = "Slide Group"
        verbose_name_plural = "Slide Groups"


class Slide(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(
        verbose_name="ID",
        editable=False,
        primary_key=True,
        unique=True,
    )
    uuid = models.UUIDField(
        primary_key=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=False,
    )
    patient = models.ForeignKey(
        to=Patient,
        on_delete=models.CASCADE,
        related_name="Patient_Slides",
        verbose_name="Ambulatory ID",
        null=True,
        blank=True,
    )
    orginization = models.CharField(
        verbose_name="Orginization",
        max_length=100,
        null=True,
        blank=False,
    )
    department = models.CharField(
        verbose_name="Department",
        max_length=50,
        null=True,
        blank=True,
    )
    organ = models.CharField(
        verbose_name="Organ",
        max_length=50,
        null=True,
        blank=True,
    )
    block_group = models.ForeignKey(
        to="BlockGroup",
        related_name="BlockGroup",
        on_delete=models.CASCADE,
        verbose_name="Block Group",
        max_length=20,
        null=True,
        blank=True,
    )

    slide_group = models.ForeignKey(
        to="SlideGroup",
        on_delete=models.CASCADE,
        verbose_name="Slide Group",
        max_length=20,
        null=True,
        blank=True,
    )

    block = models.ManyToManyField(
        to="Block",
        related_name="Block_Slides",
        verbose_name="Block Number",
        max_length=20,
        blank=True,
    )

    code = models.CharField(
        verbose_name="Slide Code (New)",
        unique=True,
        max_length=20,
        null=True,
        blank=True,
        error_messages={"unique": "Эти коды для МП уже существуют."},
    )

    information = models.CharField(
        verbose_name="Information",
        max_length=200,
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

    def __str__(self) -> str:
        identifier = str(self.code)
        return identifier

    class Meta:
        db_table = "Slide"
        verbose_name_plural = "Slides"
