from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from task_board.models import Task, Worker


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "task_type",
            "assignees",
            "deadline",
            "priority"
        ]
        labels = {
            "name": "Task Title",
            "description": "Description",
            "task_type": "Task Type",
            "assignees": "Assignees",
            "deadline": "Deadline",
            "priority": "Priority"
        }
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Task details..."}
            ),
            "deadline": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now().date():
            raise ValidationError("Deadline cannot be in the past.")
        return deadline


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )

        widgets = {
            "position": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "height: auto; min-height: 40px; font-size: 1rem;"
                }
            )
        }
