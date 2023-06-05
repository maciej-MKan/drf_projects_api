# Create your views here.
from rest_framework import viewsets, permissions

from projects_manager.project.models import Project
from projects_manager.project.serializers import ProjectDetailSerializer, ProjectModifySerializer, \
    ProjectCreateSerializer, ProjectDeleteSerializer


class ProjectAccessPermission(permissions.BasePermission):
    def __init__(self):
        self.message = 'User can modify self projects only'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.id == obj.author.id:
            return True
        if (request.method == 'GET') & (request.user in obj.users.all()):
            return True
        else:
            self.message = "You don't have permission to get this project"
        return False


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-start_date')
    permission_classes = [ProjectAccessPermission]

    def get_serializer_class(self):
        method_serializer_map = {
            'GET': ProjectDetailSerializer,
            'POST': ProjectCreateSerializer,
            'DELETE': ProjectDeleteSerializer
        }
        serializer = method_serializer_map.get(self.request.method, ProjectModifySerializer)
        print(serializer)
        return serializer
