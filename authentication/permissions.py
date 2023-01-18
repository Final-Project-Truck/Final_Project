from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'delete']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        #return obj.client == request.user.client
        return obj.creator == request.user.baseuser
