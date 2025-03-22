from django.urls import path
from task_board.views import index, WorkerListView, TaskDetailView

urlpatterns = [
    path("", index, name="index"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]

app_name = "task_board"
