from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        try:
            owner = getattr(obj, 'owner')
        except AttributeError:
            owner = getattr(obj.course, 'owner')
        if request.method in permissions.SAFE_METHODS:
            return True
        return owner == request.user
    
class IsCourseOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a course to edit it
    """

    def has_object_permission(self, request, view, obj):
        #obj could be course or lesson
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        else: 
            return obj.course.owner == request.user
        
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    