from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

from task_board.models import Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type")

    current_year = datetime.now().year

    paginator = Paginator(tasks, 6)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {
        "tasks": tasks,
        "current_year": current_year,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "paginator": paginator,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        paginator = Paginator(tasks, 6)

        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        context["page_obj"] = page_obj
        context["paginator"] = paginator
        context["is_paginated"] = page_obj.has_other_pages()

        return context
