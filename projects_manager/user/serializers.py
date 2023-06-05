import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email, RegexValidator, MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    password = serializers.CharField(write_only=True, allow_blank=False, validators=[validate_password])
    email = serializers.CharField(validators=[validate_email])
    first_name = serializers.CharField(validators=[name_validator])
    last_name = serializers.CharField(validators=[name_validator])
    age = serializers.IntegerField(validators=[age_validator])
    phone_number = serializers.CharField(validators=[phone_validator])

    class Meta:
        model = ProjectUser
        fields = ['first_name', 'last_name', 'age', 'gender', 'email', 'password', 'phone_number']


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
                raise serializers.ValidationError({'password': e.detail})
        else:
            validated_data['password'] = instance.password

        return super().update(instance, validated_data)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['id', 'first_name', 'last_name']
