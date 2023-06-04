from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProjectUserCreationForm, ProjectUserChangeForm
from .models import ProjectUser


class ProjectUserAdmin(UserAdmin):
    add_form = ProjectUserCreationForm
    form = ProjectUserChangeForm
    model = ProjectUser

    list_display = ("email", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "first_name", "last_name", "age", "gender", "phone_number",
                "is_staff", "is_active", "user_permissions"
            )}
         ),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(ProjectUser, ProjectUserAdmin)
