from django import forms

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


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            "first_name",
            "last_name",
            "email",
            "position",
            "username",
            "password"
        ]
        widgets = {
            "position": forms.Select(
                attrs={"class": "form-control"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            )
        }
