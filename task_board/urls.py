from django.urls import path
from task_board.views import (
    index,
    WorkerListView,
    TaskDetailView,
    WorkerDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]

app_name = "task_board"
