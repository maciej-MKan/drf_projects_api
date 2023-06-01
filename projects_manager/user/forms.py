from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ProjectUser


class ProjectUserCreationForm(UserCreationForm):
    class Meta:
        model = ProjectUser
        fields = ("email",)


class ProjectUserChangeForm(UserChangeForm):
    class Meta:
        model = ProjectUser
        fields = ("email",)
