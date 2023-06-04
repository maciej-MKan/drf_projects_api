from django.db import models


# Create your models here.

class Comment(models.Model):

    project = models.ForeignKey("project.Project", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("user.ProjectUser", on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1200, blank=False, null=False)
    timestamp = models.IntegerField(blank=False)

    def __str__(self):
        return 'comment for ' + str(self.project) + ' by ' + str(self.user)
