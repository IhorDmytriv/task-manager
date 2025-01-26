from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Position Model
class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Worker Model
class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="workers"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


# TaskType Model
class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Task Model
class Task(models.Model):
    task_type = models.ForeignKey(
        TaskType, on_delete=models.PROTECT, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH.USER.MODEL,
        related_name="tasks"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)

    class PriorityChoices(models.TextChoices):
        LOW = "Low", "Low Priority"
        MEDIUM = "Medium", "Medium Priority"
        HIGH = "High", "High Priority"

    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices,
        default=PriorityChoices.MEDIUM,
    )

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"
