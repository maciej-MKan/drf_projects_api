from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email, RegexValidator, MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ProjectUser
from ..project.models import Project


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(validators=[validate_email])
    first_name = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[A-Za-z]+$',
            message='First name must contain only letters.'
        )
    ])

    last_name = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[A-Za-z]+$',
            message='Last name must contain only letters.'
        )
    ])

    age = serializers.IntegerField(validators=[
        MinValueValidator(18, message='Age must be at least 18.'),
        MaxValueValidator(100, message='Age cannot exceed 100.')
    ])

    phone_number = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^(?:\+\d{1,3}\s?)?\d{9}$',
            message='Phone number must be a valid phone number with optional country code.'
        )
    ])

    class Meta:
        model = ProjectUser
        fields = ['id', 'first_name', 'last_name', 'age', 'gender', 'email', 'password', 'phone_number', 'projects']

    def to_representation(self, instance):
        request = self.context['request']
        user = request.user
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

        if validated_data.get('password', None):
            try:
                validate_password(validated_data['password'])
                validated_data['password'] = make_password(validated_data['password'])
            except ValidationError as e:
                raise serializers.ValidationError({'password': e.detail})
        else:
            validated_data['password'] = instance.password

        return super().update(instance, validated_data)

    def create(self, validated_data):
        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.detail})

        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    pass
