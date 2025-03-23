from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

from task_board.models import Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type")
    current_year = datetime.now().year
    context = {
        "tasks": tasks,
        "current_year": current_year,
    }
    return render(request, "task_board/index.html", context=context)


class TaskDetailView(DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees__position")


class WorkerListView(ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 6


class WorkerDetailView(DetailView):
    model = Worker
    queryset = Worker.objects.select_related(
        "position"
    ).prefetch_related("tasks__task_type")
