from rest_framework import permissions, viewsets

from projects_manager.comment.models import Comment
from projects_manager.comment.serializers import CommentSerializer, CommentModifySerializer


# Create your views here.


class SomePermission(permissions.BasePermission):  # ToDo: Better name
    message = 'User can modify self projects only'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    permission_classes = [SomePermission]

    def get_serializer_class(self):
        serializer = CommentModifySerializer
        if self.request.method in ['GET', ]:
            serializer = CommentSerializer
        return serializer
