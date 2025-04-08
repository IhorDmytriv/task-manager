from django.urls import path
from task_board.views import (
    index,
    TaskDetailView,
    TaskCreateView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    TaskTypeListView,
    TaskTypeCreateView,
    PositionListView,
    PositionCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("task_types", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path("positions", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
]

app_name = "task_board"
