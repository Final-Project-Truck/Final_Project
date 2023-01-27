from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            if view.action in ['create']:
                return False
            else:
                return True
        elif request.user.baseuser.user_type == "per":
            return obj.creator == request.user.baseuser
        elif request.user.baseuser.user_type == "com":
            return obj.company.base_user == request.user.baseuser


class IsSurveyOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return False
        elif request.user.baseuser:
            if obj.submitter:
                return obj.submitter == request.user.baseuser
            elif obj.survey:
                return obj.survey.creator == request.user.baseuser


class IsSubmissionOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return False
        elif request.user.baseuser:
            return obj.submission.submitter == request.user.baseuser


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return True
