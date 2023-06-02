from rest_framework import permissions, viewsets

from projects_manager.user.models import ProjectUser
from projects_manager.user.serializers import UserSerializer, UserUpdateSerializer


class UserSelfDataPermission(permissions.BasePermission):
    message = 'User can modify self data only'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        method = request.method
        if method == 'GET' or request.user.is_superuser:
            return True
        if obj == request.user:
            return True
        return False


class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = ProjectUser.objects.all().order_by('-date_joined')
    permission_classes = [UserSelfDataPermission]

    def get_serializer_class(self):
        serializer = UserSerializer
        if self.request.method in ['PUT', 'PATCH']:
            serializer = UserUpdateSerializer
        print(serializer)
        return UserSerializer
