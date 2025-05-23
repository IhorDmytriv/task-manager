from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_board.models import Position


class PrivatePositionViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    # Position List View Tests
    def test_list_displays_position(self):
        Position.objects.create(name="Python Developer")
        Position.objects.create(name="Java Developer")

        response = self.client.get(reverse("task_board:position-list"))

        self.assertEqual(response.status_code, 200)

        position = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(position)
        )
        self.assertTemplateUsed(response, "task_board/position_list.html")

    def test_filtered_position_list_displays_by_name(self):
        Position.objects.create(name="Python Developer")
        Position.objects.create(name="Java Developer")
        Position.objects.create(name="UX Designer")

        response = self.client.get(reverse("task_board:position-list") + "?name=developer")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")
        self.assertContains(response, "Java Developer")
        self.assertNotContains(response, "UX Designer")

    def test_position_list_context_contains_search_form_with_initial_value(self):
        response = self.client.get(reverse("task_board:position-list") + "?name=test")
        form = response.context["search_form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.initial["name"], "test")

    # Position Create View Tests
    def test_create_position(self):
        response = self.client.post(
            reverse("task_board:position-create"),
            {"name": "Python Developer"}
        )
        self.assertEqual(Position.objects.count(), 1)
        self.assertRedirects(response, reverse("task_board:position-list"))

    # Position Update View Tests
    def test_update_position(self):
        position = Position.objects.create(name="Old name")
        response = self.client.post(
            reverse("task_board:position-update", args=[position.id]),
            {"name": "New name"}
        )
        position.refresh_from_db()
        self.assertEqual(position.name, "New name")
        self.assertRedirects(response, reverse("task_board:position-list"))

    # Position Delete View Tests
    def test_delete_position(self):
        position = Position.objects.create(name="Test position")
        response = self.client.post(
            reverse("task_board:position-delete", args=[position.id])
        )
        self.assertFalse(Position.objects.filter(id=position.id).exists())
        self.assertRedirects(response, reverse("task_board:position-list"))


class PublicPositionViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Python Developer")

    def test_login_required_position_list(self):
        response = self.client.get(reverse("task_board:position-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_position_create(self):
        response = self.client.get(reverse("task_board:position-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_position_update(self):
        response = self.client.get(reverse("task_board:position-update", args=[self.position.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_position_delete(self):
        response = self.client.get(reverse("task_board:position-delete", args=[self.position.id]))
        self.assertNotEqual(response.status_code, 200)
