from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_board.models import Position, Task, Worker, TaskType


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {"fields": ("first_name", "last_name", "position", "email")}
        ),
    )


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_complete",
    ]
    list_filter = ["task_type", "priority", "deadline", "is_complete", ]
    search_fields = ["name", ]


admin.site.unregister(Group)
