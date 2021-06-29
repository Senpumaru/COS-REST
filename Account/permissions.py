from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

## User permissions
class IsGuest(permissions.BasePermission):
    """
    Guest credentials
    """
    message = "Guests can only browse data!"

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_guest):
            return True
        return False

EXPANDED_METHODS = ['GET', "POST", 'HEAD', 'OPTIONS']

class IsRegistrator(permissions.BasePermission):
    """
    Registrator credentials
    """
    message = "You require minimal Registrator persmissions!"

    def has_permission(self, request, view):
        
        if (request.method in EXPANDED_METHODS or
            request.user and
            request.user.is_registrator):
            return True
        return False


class IsConsultant(permissions.BasePermission):
    """
    Consultant credentials
    """
    message = "You require minimal Consultant persmissions!"

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_consultant):
            return True
        return False


class IsClinician(permissions.BasePermission):
    """
    Clinicians credentials
    """

    message = "You require minimal Clinician persmissions!"

    def has_permission(self, request, view):
        print("Clinician Check.")
        return bool(request.user and request.user.is_clinician)


class IsPathologist(permissions.BasePermission):
    """
    Pathologists credentials
    """

    message = "You require minimal Pathologist persmissions!"

    def has_permission(self, request, view):
        print("Pathologist Check.")
        return bool(request.user and request.user.is_pathologist)

## Application permissions
class AccessST0001(permissions.BasePermission):
    """
    ST0001 permissions
    """

    message = "You require minimal ST0001 persmissions!"

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.ST0001_allow)
    
class AccessST0002(permissions.BasePermission):
    """
    ST0002 permissions
    """

    message = "You require minimal ST0002 persmissions!"

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.ST0002_allow)
