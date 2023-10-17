from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsAuthorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (obj.author == user or request.method in SAFE_METHODS
                or user.is_staff or user.is_admin)
