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
    # Credential types
    is_guest = models.BooleanField(
        verbose_name="Guest Status",
        default=True,
        help_text="Designates basic permissions for guests's access.",
    )
    is_registrator = models.BooleanField(
        verbose_name="Registrator Status",
        default=False,
        help_text="Designates  permissions for registrator's access.",
    )
    is_consultant = models.BooleanField(
        verbose_name="Consultant Status",
        default=False,
        help_text="Designates permissions for consultant's access.",
    )
    is_clinician = models.BooleanField(
        verbose_name="Clinician Status",
        default=False,
        help_text="Designates permissions for clinician's access.",
    )
    is_pathologist = models.BooleanField(
        verbose_name="Pathologist Status",
        default=False,
        help_text="Designates elevated permissions for pathologist's access.",
    )
    # App types
    ST0001_allow = models.BooleanField(
        verbose_name="Application for IHC:ALK cases",
        default=False,
        help_text="Gives access to ST0001 application.",
    )
    ST0002_allow = models.BooleanField(
        verbose_name="Application for IHC:PDL1 cases",
        default=False,
        help_text="Gives access to ST0002 application.",
    )
    
    ## Frontend Specific Rights ##
        
    @property
    def credentials_status(self):
        "Class granted by admin."
        credential_stati = {}
        if self.is_guest == True:
            credential_stati["Guest"] = True
        if self.is_registrator == True:
            credential_stati["Registrator"] = True
        if self.is_consultant == True:
            credential_stati["Consultant"] = True
        if self.is_clinician == True:
            credential_stati["Clinician"] = True
        if self.is_pathologist == True:
            credential_stati["Pathologist"] = True
        if self.is_staff == True:
            credential_stati["Staff"] = True
        return credential_stati
    
    @property
    def application_rights(self):
        apps = {
            "ST0001":False,
            "ST0002":False,
        }
        if self.ST0001_allow == True:
            apps["ST0001"] = True
        if self.ST0002_allow == True:
            apps["ST0002"] = True
        return apps
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ServiceUserManager()

    def __str__(self):
        return " ".join([self.first_name, self.last_name, "(" + self.email + ")"])
