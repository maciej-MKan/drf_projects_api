# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from ..project.models import Project


class ProjectUser(AbstractUser):

    GENDERS = (
        ("Ms", "female"),
        ("Mr", "male")
    )

    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=500, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDERS)
    phone_number = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def projects(self):
        return Project.objects.filter(users=self)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
