from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from task_board.models import TaskType


class PrivateTaskTypeViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    # TaskType List View Tests
    def test_list_displays_task_types(self):
        TaskType.objects.create(name="Bug Fix")
        TaskType.objects.create(name="New Feature")

        response = self.client.get(reverse("task_board:task-type-list"))

        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types)
        )
        self.assertTemplateUsed(response, "task_board/task_type_list.html")

    def test_filtered_task_list_displays_task_types_by_name(self):
        TaskType.objects.create(name="Fix login bug")
        TaskType.objects.create(name="Refactor login")
        TaskType.objects.create(name="Improve UI")

        response = self.client.get(reverse("task_board:task-type-list") + "?name=login")

        self.assertContains(response, "Fix login bug")
        self.assertContains(response, "Refactor login")
        self.assertNotContains(response, "Improve UI")

    def test_task_list_context_contains_search_form_with_initial_value(self):
        response = self.client.get(reverse("task_board:task-type-list") + "?name=test")
        form = response.context["search_form"]
        self.assertEqual(form.initial["name"], "test")

    # TaskType Create View Tests
    def test_create_task_type(self):
        response = self.client.post(
            reverse("task_board:task-type-create"),
            {"name": "Bug Fix"}
        )
        self.assertEqual(TaskType.objects.count(), 1)
        self.assertRedirects(response, reverse("task_board:task-type-list"))

    # TaskType Update View Tests
    def test_update_task_type(self):
        task_type = TaskType.objects.create(name="Old name")
        response = self.client.post(
            reverse("task_board:task-type-update", args=[task_type.id]),
            {"name": "New name"}
        )
        task_type.refresh_from_db()
        self.assertEqual(task_type.name, "New name")
        self.assertRedirects(response, reverse("task_board:task-type-list"))

    # TaskType Delete View Tests
    def test_delete_task_type(self):
        task_type = TaskType.objects.create(name="Bug Fix")
        response = self.client.post(
            reverse("task_board:task-type-delete", args=[task_type.id])
        )
        self.assertFalse(TaskType.objects.filter(id=task_type.id).exists())
        self.assertRedirects(response, reverse("task_board:task-type-list"))


class PublicTaskTypeViewTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bugfix")

    def test_login_required_task_type_list(self):
        response = self.client.get(reverse("task_board:task-type-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_type_create(self):
        response = self.client.get(reverse("task_board:task-type-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_type_update(self):
        response = self.client.get(reverse("task_board:task-type-update", args=[self.task_type.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_type_delete(self):
        response = self.client.get(reverse("task_board:task-type-delete", args=[self.task_type.id]))
        self.assertNotEqual(response.status_code, 200)
