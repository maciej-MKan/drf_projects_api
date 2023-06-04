from rest_framework import serializers

from ..comment.serializers import CommentSerializer
from ..project.models import Project
from ..user.serializers import UserNameSerializer


class ProjectSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 'author']


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()
    users = UserNameSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 'author', 'users', 'comments']


class ProjectNameSerializer(serializers.ModelSerializer):
    model = Project
    fields = ['id', 'name']
