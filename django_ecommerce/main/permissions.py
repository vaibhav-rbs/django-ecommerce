from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
    
        return obj.user == request.user