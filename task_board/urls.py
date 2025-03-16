from django.urls import path
from task_board.views import index, WorkerListView

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]

app_name = "task_board"
