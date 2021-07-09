from rest_framework import permissions

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

## User permissions
class Guest(permissions.BasePermission):
    """
    Guest credentials
    """

    message = "Guests can only browse data!"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user and request.user.ST1010_Permission.guest:
            return True
        return False


EXPANDED_METHODS = ["GET", "POST", "HEAD", "OPTIONS"]


class Registrar(permissions.BasePermission):
    """
    registrar credentials
    """

    message = "You require minimal registrar persmissions!"

    def has_permission(self, request, view):

        if request.method in EXPANDED_METHODS or request.user and request.user.ST1010_Permission.registrar:
            return True
        return False


class Consultant(permissions.BasePermission):
    """
    Consultant credentials
    """

    message = "You require minimal Consultant persmissions!"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user and request.user.ST1010_Permission.consultant:
            return True
        return False


class Clinician(permissions.BasePermission):
    """
    Clinicians credentials
    """

    message = "You require minimal Clinician persmissions!"

    def has_permission(self, request, view):
        print("Clinician Check.")
        return bool(request.user and request.user.ST1010_Permission.clinician)


class Pathologist(permissions.BasePermission):
    """
    Pathologists credentials
    """

    message = "You require minimal Pathologist persmissions!"

    def has_permission(self, request, view):
        print("Pathologist Check.")
        return bool(request.user and request.user.ST1010_Permission.pathologist)
