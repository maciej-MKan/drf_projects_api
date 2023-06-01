from rest_framework import serializers
from .models import ProjectUser
from ..project.models import Project


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = ProjectUser
        fields = ['first_name', 'last_name', 'password', 'age', 'gender', 'email', 'phone_number', 'projects']
