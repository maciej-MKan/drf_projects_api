from rest_framework import permissions, viewsets

from projects_manager.user.models import ProjectUser
from projects_manager.user.serializers import UserSerializer, UserModifySerializer, UserCreateSerializer


class UserSelfDataPermission(permissions.BasePermission):

    def __init__(self):
        self.message = 'You can modify self data only'

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        method = request.method
        if (method == 'DELETE') and not request.user.is_superuser:
            self.message = "Only admin can delete users"
            return False
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
        request_serializer_map = {
            'POST': UserCreateSerializer,
            'PUT': UserModifySerializer,
            'PATCH': UserModifySerializer
        }
        return request_serializer_map.get(self.request.method, UserSerializer)
