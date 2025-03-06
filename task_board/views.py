from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from task_board.models import Task


def index(request: HttpRequest) -> HttpResponse:
    task_list = Task.objects.all()
    context = {
        "task_list": task_list
    }
    return render(request, "task_board/index.html", context=context)
