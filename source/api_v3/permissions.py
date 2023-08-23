from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAuthor(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve" or request.user == obj.author:
            return True
        return False
