from django.db import models

from projects_manager.comment.models import Comment


# Create your models here.
class Project(models.Model):
    STATUS = (
        ("NEW", "NEW"),
        ("PENDING", "In pending"),
        ("PROGRESS", "In progress"),
        ("COMPLETED", "Completed"),
    )

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    start_date = models.IntegerField(blank=False)
    end_date = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=12, choices=STATUS, default="NEW", blank=False)
    author = models.ForeignKey("user.ProjectUser", on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField("user.ProjectUser", related_name="user")

    def __str__(self):
        return str(self.name) + " by " + str(self.author)

    @property
    def comments(self):
        return Comment.objects.filter(project=self)
