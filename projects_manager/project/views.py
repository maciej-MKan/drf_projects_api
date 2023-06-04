# Create your views here.
from rest_framework import viewsets, permissions

from projects_manager.project.models import Project
from projects_manager.project.serializers import ProjectDetailSerializer


class SomePermission(permissions.BasePermission):  # ToDo: Better name
    message = 'User can modify self projects only'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-start_date')
    permission_classes = [SomePermission]

    def get_serializer_class(self):
        return ProjectDetailSerializer
