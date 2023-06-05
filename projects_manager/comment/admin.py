from django.contrib import admin

from projects_manager.comment.models import Comment


# Register your models here.
@admin.register(Comment)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'comment', 'timestamp']
    list_filter = ['project', 'user']
    search_fields = ['project', 'user']

