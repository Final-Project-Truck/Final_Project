from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user.baseuser


class IsSurveyOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.survey.creator == request.user.baseuser
