from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _


class ServiceUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # Protected password
        user.editable_password = False
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class ServiceUser(AbstractUser):
    username = None
    email = models.EmailField(_("Email Address"), unique=True)
    ## Backend Specific Rights ##

    # App types
    ST1010_allow = models.BooleanField(
        verbose_name="Application for IHC:ALK cases",
        default=False,
        help_text="Gives access to ST1010 application.",
    )
    ST1011_allow = models.BooleanField(
        verbose_name="Application for IHC:PDL1 cases",
        default=False,
        help_text="Gives access to ST1011 application.",
    )

    ## Frontend Specific Rights ##

    @property
    def application_rights(self):
        apps = {
            "ST1010": False,
            "ST1011": False,
        }
        if self.ST1010_allow == True:
            apps["ST1010"] = True
        if self.ST1011_allow == True:
            apps["ST1011"] = True
        return apps

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ServiceUserManager()

    def __str__(self):
        return " ".join([self.first_name, self.last_name, "(" + self.email + ")"])


class ST1010_Permission(models.Model):
    user = models.OneToOneField(
        to=ServiceUser,
        related_name="ST1010_Permission",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    # Credential types
    guest = models.BooleanField(
        verbose_name="Guest Status",
        default=True,
        help_text="ST1010 permissions for Guests's access.",
    )
    registrar = models.BooleanField(
        verbose_name="Registrar Status",
        default=False,
        help_text="ST1010 permissions for Registrar's access.",
    )
    consultant = models.BooleanField(
        verbose_name="Consultant Status",
        default=False,
        help_text="ST1010 permissions for Consultant's access.",
    )
    clinician = models.BooleanField(
        verbose_name="Clinician Status",
        default=False,
        help_text="ST1010 permissions for Clinician's access.",
    )
    pathologist = models.BooleanField(
        verbose_name="Pathologist Status",
        default=False,
        help_text="ST1010 elevated permissions for Pathologist's access.",
    )

    def __str__(self):
        return " ".join([self.user.first_name, self.user.last_name, "(" + self.user.email + ")"])

    class Meta:
        db_table = "ST1010 Permission"
        verbose_name_plural = "ST1010 Permissions"

    @property
    def credentials_status(self):
        "Class granted by admin."
        credential_stati = {}
        if self.guest == True:
            credential_stati["Guest"] = True
        if self.registrar == True:
            credential_stati["Registrar"] = True
        if self.consultant == True:
            credential_stati["Consultant"] = True
        if self.clinician == True:
            credential_stati["Clinician"] = True
        if self.pathologist == True:
            credential_stati["Pathologist"] = True
        if self.is_staff == True:
            credential_stati["Staff"] = True
        return credential_stati
