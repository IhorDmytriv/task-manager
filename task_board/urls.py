from django.urls import path
from task_board.views import (
    index,
    WorkerListView,
    TaskDetailView,
    WorkerDetailView,
    TaskCreateView,
    TaskTypeListView,
    PositionListView,
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
    path("task_types", TaskTypeListView.as_view(), name="task-type-list"),
    path("positions", PositionListView.as_view(), name="position-list"),
]

app_name = "task_board"
