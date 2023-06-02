from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import ProjectUser
from ..project.models import Project


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = ProjectUser
        fields = ['id', 'first_name', 'last_name', 'age', 'gender', 'email', 'password', 'phone_number', 'projects']

    def to_representation(self, instance):
        request = self.context['request']
        user = request.user
        # if request.method == "GET":
        instance.password = ""

        if not user.is_superuser and user != instance:
            if instance.is_superuser:
                return {}
            return {
                'id': instance.id,
                'first_name': instance.first_name,
                'last_name': instance.last_name
            }
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        return super().update(instance, validated_data)

