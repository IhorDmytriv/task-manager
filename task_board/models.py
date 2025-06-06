from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Position Model
class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Worker Model
class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE, related_name="workers",
        null=True, blank=True,
        default=None,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}, ({self.position})"

    def get_absolute_url(self):
        return reverse("task_board:worker-detail", kwargs={"pk": self.id})


# TaskType Model
class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Task Model
class Task(models.Model):
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    PRIORITY_CHOICES = [
        (3, "High Priority"),
        (2, "Medium Priority"),
        (1, "Low Priority"),
    ]

    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"

    def get_absolute_url(self):
        return reverse("task_board:task-detail", kwargs={"pk": self.id})
