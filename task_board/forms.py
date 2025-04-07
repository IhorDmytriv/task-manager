from django import forms

from task_board.models import Task


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
