from rest_framework import permissions, viewsets

from projects_manager.user.models import ProjectUser
from projects_manager.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = ProjectUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
