from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="member").exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="member").exists():
            return True
        return False


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        try:
            if obj.user:
                if obj.user == request.user:
                    return True
        except:
            if obj == request.user:
                return True
            return False
