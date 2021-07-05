from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

## Application permissions
class AccessST1010(permissions.BasePermission):
    """
    ST1010 permissions
    """

    message = "You require minimal ST1010 persmissions!"

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.ST1010_allow)
    
class AccessST1011(permissions.BasePermission):
    """
    ST1011 permissions
    """

    message = "You require minimal ST1011 persmissions!"

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.ST1011_allow)
