from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from task_board.forms import TaskForm
from task_board.models import Task, Worker, TaskType, Position


@login_required
def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type")

    current_year = datetime.now().year

    paginator = Paginator(tasks, 6)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "tasks": tasks,
        "current_year": current_year,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "paginator": paginator,
        "num_visits": num_visits + 1,
    }
    return render(request, "task_board/index.html", context=context)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees__position")
    )


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_board:index")
    template_name = "task_board/task_form.html"


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 6


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    queryset = (
        Worker.objects
        .select_related("position")
        .prefetch_related("tasks__task_type")
    )

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

class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "task_board/task_type_list.html"
    context_object_name = "task_type_list"

class PositionListView(LoginRequiredMixin, ListView):
    model = Position
