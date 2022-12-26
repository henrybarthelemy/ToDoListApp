from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    finished = models.BooleanField(default=False)
    # user which created this task
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse("task-update", kwargs={"id": self.id})
