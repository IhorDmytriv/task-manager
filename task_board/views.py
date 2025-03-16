from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from task_board.models import Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type")
    current_year = datetime.now().year
    context = {
        "tasks": tasks,
        "current_year": current_year,
    }
    return render(request, "task_board/index.html", context=context)


class WorkerListView(ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
