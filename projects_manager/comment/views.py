from rest_framework import permissions, viewsets

from projects_manager.comment.models import Comment
from projects_manager.comment.serializers import CommentSerializer, CommentModifySerializer, CommentCreateSerializer
from projects_manager.project.models import Project


class CommentAccessPermission(permissions.BasePermission):

    def __init__(self):
        self.message = 'User can add comments only to assigned projects'

    def has_permission(self, request, view):
        if request.user not in Project(request.data['project']).users.all():
            return False
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method not in ['GET', 'POST']:
            self.message = "You can only add and show comments"
            return False
        if request.user in obj.project.users.all():
            return True
        return False


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    permission_classes = [CommentAccessPermission]

    def get_serializer_class(self):
        request_serializer_map = {
            "POST": CommentCreateSerializer,
            "PUT": CommentModifySerializer,
            "PATCH": CommentModifySerializer
        }
        return request_serializer_map.get(self.request.method, CommentSerializer)
