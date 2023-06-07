import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import ProjectUser


def name_validator(name):
    pattern = r'^[A-Za-z]+$'
    if not re.match(pattern, name):
        raise ValidationError('Must contain only letters.')


def age_validator(age):
    if age < 18:
        raise ValidationError('Age must be at least 18.')
    if age > 100:
        raise ValidationError('Age cannot exceed 100.')


def phone_validator(number):
    pattern = r'^(?:\+\d{1,3}\s?)?\d{9}$'
    if not re.match(pattern, number):
        raise ValidationError('Phone number must be a valid phone number with optional country code.')


def custom_password_validator(value):
    try:
        validate_password(value)
    except ValidationError:
        raise ValidationError('You must type beater password')


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProjectUser
        fields = ['id', 'first_name', 'last_name', 'age', 'gender', 'email', 'phone_number', 'projects']

    def get_projects(self, obj):
        from ..project.serializers import ProjectSerializer
        serializer = ProjectSerializer(obj.projects, many=True)
        return serializer.data

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


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100,
        write_only=True,
        allow_blank=False,
        validators=[custom_password_validator]
    )
    email = serializers.CharField(max_length=30, validators=[validate_email])
    first_name = serializers.CharField(validators=[name_validator])
    last_name = serializers.CharField(validators=[name_validator])
    age = serializers.IntegerField(validators=[age_validator])
    phone_number = serializers.CharField(validators=[phone_validator], allow_blank=True)

    class Meta:
        model = ProjectUser
        fields = ['first_name', 'last_name', 'age', 'gender', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def handle_exception(self, exc):
        if isinstance(exc, serializers.ValidationError):
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class UserModifySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, allow_blank=True)
    email = serializers.CharField(validators=[validate_email])
    first_name = serializers.CharField(validators=[name_validator])
    last_name = serializers.CharField(validators=[name_validator])
    age = serializers.IntegerField(validators=[age_validator])
    phone_number = serializers.CharField(validators=[phone_validator])

    class Meta:
        model = ProjectUser
        fields = ['first_name', 'last_name', 'age', 'gender', 'email', 'password', 'phone_number']

    def update(self, instance, validated_data):

        if validated_data.get('password', None):
            try:
                validate_password(validated_data['password'])
                validated_data['password'] = make_password(validated_data['password'])
            except ValidationError as e:
                raise ValidationError({'password': e.detail})
        else:
            validated_data['password'] = instance.password

        return super().update(instance, validated_data)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['id', 'first_name', 'last_name']
