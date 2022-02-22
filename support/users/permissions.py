from rest_framework import permissions


# permission for user's own tickets
class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


