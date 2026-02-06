from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только для владельца"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """Разрешение только для владельца"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicOrOwner(permissions.BasePermission):
    """Разрешение на просмотр публичных или своих привычек"""

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.user == request.user
