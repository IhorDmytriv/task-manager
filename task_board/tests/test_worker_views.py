from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_board.models import Worker, Position


class PrivateWorkerViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

        self.position_1 = Position.objects.create(name="Python Developer")
        self.position_2 = Position.objects.create(name="Java Developer")
        self.position_3 = Position.objects.create(name="UX/UI Designer")

        self.worker_1 = get_user_model().objects.create_user(
            username="test_worker_1",
            password="test123",
            first_name="Python",
            last_name="Developer 1",
            position=self.position_1
        )

        self.worker_2 = get_user_model().objects.create_user(
            username="test_worker_2",
            password="test123",
            first_name="Java",
            last_name="Developer 2",
            position=self.position_2
        )

        self.worker_3 = get_user_model().objects.create_user(
            username="test_worker_3",
            password="test123",
            first_name="UX/UI",
            last_name="Designer",
            position=self.position_3
        )

    # Worker List View Tests
    def test_worker_list_displays_workers(self):
        response = self.client.get(reverse("task_board:worker-list"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["worker_list"]),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(response, "task_board/worker_list.html")

    def test_worker_list_context_contains_search_form_with_initial_value(self):
        response = self.client.get(
            reverse("task_board:worker-list") + "?first_name=test_first_name&last_name=test_last_name"
        )
        form = response.context["search_form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.initial["first_name"], "test_first_name")
        self.assertEqual(form.initial["last_name"], "test_last_name")

    def test_filtered_task_list_displays_by_first_name(self):
        response = self.client.get(reverse("task_board:worker-list") + "?first_name=Python")

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Python")
        self.assertNotContains(response, "Java")
        self.assertNotContains(response, "UX/UI")

    def test_filtered_task_list_displays_by_last_name(self):
        response = self.client.get(reverse("task_board:worker-list") + "?last_name=Developer")

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Developer 1")
        self.assertContains(response, "Developer 2")
        self.assertNotContains(response, "Designer")

    # Worker Detail View Test
    def test_worker_detail_displays_correct_worker_info(self):
        response = self.client.get(
            reverse("task_board:worker-detail", args=[self.worker_1.id])
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.worker_1.first_name)
        self.assertContains(response, self.worker_1.last_name)
        self.assertContains(response, self.worker_1.position)

    # Worker Create View Test
    def test_create_worker(self):
        form_data = {
            "username": "test_worker",
            "password1": "password_123",
            "password2": "password_123",
            "first_name": "Test Name",
            "last_name": "Test LastName",
            "email": "test@mail.com",
            "position": self.position_1.id

        }
        response = self.client.post(reverse("task_board:worker-create"), data=form_data)
        new_worker = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_worker.first_name, form_data["first_name"])
        self.assertEqual(new_worker.last_name, form_data["last_name"])
        self.assertEqual(new_worker.email, form_data["email"])
        self.assertEqual(new_worker.position.id, form_data["position"])

        self.assertRedirects(response, reverse("task_board:worker-list"))


class PublicWorkerViewTests(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
            first_name="Test name",
            last_name="Test surname",
            email="test@email.com",
            position=Position.objects.create(name="Python Developer")
        )

    def test_login_required_worker_list(self):
        response = self.client.get(reverse("task_board:worker-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_worker_detail(self):
        response = self.client.get(reverse("task_board:worker-detail", args=[self.worker.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_login_not_required_worker_create(self):
        response = self.client.get(reverse("task_board:worker-create"))
        self.assertEqual(response.status_code, 200)
