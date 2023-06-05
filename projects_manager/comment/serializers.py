from datetime import datetime
import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from projects_manager.comment.models import Comment
from projects_manager.project.models import Project
from projects_manager.user.serializers import UserNameSerializer


def validate_no_special_characters(value):
    pattern = r'^(?!.*[£$%&*]+.*[£$%&*]+.*[£$%&*]+)[^£$%&*]+$'
    if not re.match(pattern, value):
        raise ValidationError('The entered value is incorrect.')


def validate_comment(comment):
    if len(comment) < 10:
        raise ValidationError('Description must be at least 10 characters long.')
    if len(comment) > 500:
        raise ValidationError('Description cannot exceed 500 characters.')


class CommentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = UserNameSerializer(read_only=True)
    comment = serializers.CharField()
    timestamp = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'comment', 'timestamp']


class CommentModifySerializer(serializers.ModelSerializer):
    comment = serializers.CharField(max_length=500, allow_null=False, allow_blank=False, validators=[
        validate_comment,
        validate_no_special_characters,
    ])

    class Meta:
        model = Comment
        fields = ['comment']


class CommentCreateSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), allow_null=False, allow_empty=False)
    comment = serializers.CharField(max_length=500, allow_null=False, allow_blank=False, validators=[
        validate_comment,
        validate_no_special_characters,
    ])

    class Meta:
        model = Comment
        fields = ['project', 'comment']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        validated_data['user'] = user
        validated_data['timestamp'] = datetime.now().timestamp()
        comment = Comment.objects.create(**validated_data)
        return comment
