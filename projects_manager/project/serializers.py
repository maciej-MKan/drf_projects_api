import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..comment.serializers import CommentSerializer
from ..project.models import Project
from ..user.models import ProjectUser
from ..user.serializers import UserNameSerializer


def validate_no_special_characters(value):

    pattern = r'^(?!.*[£$%&*]+.*[£$%&*]+.*[£$%&*]+)[^£$%&*]+$'
    if not re.match(pattern, value):
        raise ValidationError('The entered value is incorrect.')


def validate_name(name):
    print("name validator")
    if len(name) < 3:
        raise ValidationError('Name must be at least 3 characters long.')
    if len(name) > 100:
        raise ValidationError('Name cannot exceed 100 characters.')


def validate_description(description):
    if len(description) < 10:
        raise ValidationError('Description must be at least 10 characters long.')
    if len(description) > 1000:
        raise ValidationError('Description cannot exceed 1000 characters.')


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


class ProjectModifySerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=ProjectUser.objects.all(), allow_null=False, allow_empty=False,
        many=True
    )
    name = serializers.CharField(max_length=100, allow_null=False, allow_blank=False, validators=[
        validate_name,
        validate_no_special_characters,
    ])
    description = serializers.CharField(max_length=1000, allow_null=False, allow_blank=False, validators=[
        validate_description,
        validate_no_special_characters,
    ])

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'users']


class ProjectCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, allow_null=False, allow_blank=False, validators=[
        validate_name,
        validate_no_special_characters,
    ])
    description = serializers.CharField(max_length=1000, allow_null=False, allow_blank=False, validators=[
        validate_description,
        validate_no_special_characters,
    ])

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        validated_data['author'] = user
        validated_data['status'] = 'NEW'
        project = Project.objects.create(**validated_data)
        project.users.add(user)
        return project


class ProjectDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id']
