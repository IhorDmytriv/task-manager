from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from task_board.models import Task


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.all()
    context = {
        "tasks": tasks
    }
    return render(request, "task_board/index.html", context=context)
