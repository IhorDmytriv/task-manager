from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from task_board.models import Task


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type")
    current_year = datetime.now().year
    context = {
        "tasks": tasks,
        "current_year": current_year,
    }
    return render(request, "task_board/index.html", context=context)
