from rest_framework import serializers

from projects_manager.comment.models import Comment
from projects_manager.project.models import Project
from projects_manager.user.serializers import UserNameSerializer


class CommentSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = UserNameSerializer()
    comment = serializers.CharField()
    timestamp = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'comment', 'timestamp']
