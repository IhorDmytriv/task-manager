from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from task_board.forms import (
    TaskForm,
    WorkerCreationForm,
    WorkerSearchForm,
    TaskSearchForm,
    NameSearchForm
)
from task_board.models import Task, Worker, TaskType, Position


@login_required
def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.select_related("task_type")

    name = request.GET.get("name", "")
    if name:
        tasks = tasks.filter(name__icontains=name)

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
        "search_form": TaskSearchForm(initial={"name": name}),
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


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_board:index")
    template_name = "task_board/task_form.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_board/task_confirm_delete.html"
    success_url = reverse_lazy("task_board:index")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        search_fields = ["first_name", "last_name"]
        initial_data = {
            field: self.request.GET.get(field, "")
            for field in search_fields
        }

        context["search_form"] = WorkerSearchForm(initial=initial_data)
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        filters = {}

        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")

        if first_name:
            filters["first_name__icontains"] = first_name
        if last_name:
            filters["last_name__icontains"] = last_name
        return queryset.filter(**filters)


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


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_board:worker-list")


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "task_board/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = NameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = super(TaskTypeListView, self).get_queryset()

        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_board/task_type_form.html"
    success_url = reverse_lazy("task_board:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_board/task_type_form.html"
    success_url = reverse_lazy("task_board:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    template_name = "task_board/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_board:task-type-list")


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = NameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = super(PositionListView, self).get_queryset()

        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_board:position-list")


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_board:position-list")


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    template_name = "task_board/position_confirm_delete.html"
    success_url = reverse_lazy("task_board:position-list")
