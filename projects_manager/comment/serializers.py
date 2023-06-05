from rest_framework import serializers

from projects_manager.comment.models import Comment
from projects_manager.project.models import Project
from projects_manager.user.models import ProjectUser
from projects_manager.user.serializers import UserNameSerializer


class CommentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = UserNameSerializer(read_only=True)
    comment = serializers.CharField()
    timestamp = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'comment', 'timestamp']


class CommentModifySerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), allow_null=False, allow_empty=False)
    user = serializers.PrimaryKeyRelatedField(queryset=ProjectUser.objects.all(), allow_null=False, allow_empty=False)
    comment = serializers.CharField()
    timestamp = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'comment', 'timestamp']
