from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_board.models import Task, TaskType


class PrivateTaskViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123"
        )
        self.client.force_login(self.user)
        self.task_type_1 = TaskType.objects.create(name="Bugfix")
        self.task_type_2 = TaskType.objects.create(name="New Feature")

        self.task_1 = Task.objects.create(
            name="Add google login button",
            description="Add google login button on sign-in page",
            task_type=self.task_type_2,
        )
        self.task_2 = Task.objects.create(
            name="Add facebook sign-up button",
            description="Add facebook sign-up button on sign-up page",
            task_type=self.task_type_2,
        )
        self.task_3 = Task.objects.create(
            name="Fix login issues",
            description="Resolve the issues where users are unable to log in.",
            task_type=self.task_type_1,
        )

    # Task List (index) View Tests
    def test_task_list_displays_tasks(self):
        response = self.client.get(reverse("task_board:index"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["page_obj"]),
            list(Task.objects.all())
        )
        self.assertTemplateUsed(response, "task_board/index.html")

    def test_filtered_task_list_displays_by_name(self):
        response = self.client.get(reverse("task_board:index") + "?name=button")

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Add google login button")
        self.assertContains(response, "Add facebook sign-up button")
        self.assertNotContains(response, "Fix login issues")

    def test_sorted_task_list_displays_by_name(self):
        response = self.client.get(reverse("task_board:index") + "?sort=name")

        self.assertEqual(response.status_code, 200)
        name_sorted_list = [
            "Add facebook sign-up button",
            "Add google login button",
            "Fix login issues"
        ]
        response_name_sorted_list = [task.name for task in response.context["page_obj"]]
        self.assertEqual(response_name_sorted_list, name_sorted_list)

    def test_task_list_context_contains_search_form_with_initial_value(self):
        response = self.client.get(reverse("task_board:index") + "?name=test")
        form = response.context["search_form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.initial["name"], "test")

    # Task toggle status View Test
    def test_toggle_task_status(self):
        self.task_1.is_complete = False
        response = self.client.post(reverse("task_board:toggle-task-status", args=[self.task_1.id]))

        self.task_1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task_1.is_complete, True)
        self.assertRedirects(response, reverse("task_board:index"))

    # Task Detail View Tests
    def test_task_detail_displays_correct_task(self):
        response = self.client.get(reverse("task_board:task-detail", args=[self.task_1.id]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.task_1.name)
        self.assertContains(response, self.task_1.description)
        self.assertContains(response, self.task_1.task_type.name)

    def test_task_detail_view_task_not_found(self):
        response = self.client.get(reverse("task_board:task-detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    # Task Create View Tests
    def test_create_task(self):
        form_data = {
            "name": "Add apple login button",
            "description": "Add apple login button on sign-in page",
            "task_type": self.task_type_2.id,
            "assignees": [self.user.id],
            "priority": 1
        }
        response = self.client.post(reverse("task_board:task-create"), data=form_data)
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(name=form_data["name"])
        self.assertEqual(task.name, form_data["name"])
        self.assertEqual(task.description, form_data["description"])
        self.assertEqual(task.task_type.id, form_data["task_type"])
        self.assertEqual(task.assignees.first().id, form_data["assignees"][0])
        self.assertEqual(task.priority, form_data["priority"])

        self.assertRedirects(response, reverse("task_board:index"))

    # Task Update View Tests
    def test_update_task(self):
        form_data = {
            "name": "New name",
            "description": "New description",
            "task_type": self.task_type_1.id,
            "assignees": [self.user.id],
            "priority": 2
        }
        response = self.client.post(
            reverse("task_board:task-update", args=[self.task_1.id]),
            data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.name, form_data["name"])
        self.assertEqual(self.task_1.description, form_data["description"])
        self.assertEqual(self.task_1.task_type.id, form_data["task_type"])
        self.assertEqual(self.task_1.priority, form_data["priority"])
        self.assertRedirects(response, reverse("task_board:index"))

    # Test Task Delete View
    def test_delete_task(self):
        response = self.client.post(reverse("task_board:task-delete", args=[self.task_1.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task_1.id).exists())
        self.assertRedirects(response, reverse("task_board:index"))


class PublicTaskViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="Add google login button",
            description="Add google login button on sign-in page",
            task_type=TaskType.objects.create(name="Bugfix"),
        )

    def test_login_required_task_list(self):
        response = self.client.get(reverse("task_board:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_detail(self):
        response = self.client.get(reverse("task_board:task-detail", args=[self.task.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_create(self):
        response = self.client.get(reverse("task_board:task-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_update(self):
        response = self.client.get(reverse("task_board:task-update", args=[self.task.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_delete(self):
        response = self.client.get(reverse("task_board:task-delete", args=[self.task.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task_toggle_task_status(self):
        response = self.client.get(reverse("task_board:toggle-task-status", args=[self.task.id]))
        self.assertNotEqual(response.status_code, 200)
