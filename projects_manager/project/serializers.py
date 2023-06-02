from rest_framework import serializers
from ..project.models import Project


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'author']
