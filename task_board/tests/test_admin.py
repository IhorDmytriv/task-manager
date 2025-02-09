from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_board.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Python Developer")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="worker123",
            position=self.position,
        )

    def test_worker_position_displayed_in_list_view(self):
        """
        Test that worker`s position is in list_display on worker admin page.
        """
        url = reverse('admin:task_board_worker_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_worker_position_displayed_in_detail_view(self):
        """
        Test that worker`s position is on worker detail admin page.
        """
        url = reverse('admin:task_board_worker_change', args=[self.worker.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_worker_position_displayed_in_create_view(self):
        """
        Test that worker`s position is on worker add admin page.
        """
        url = reverse('admin:task_board_worker_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_worker_position_filter_in_list_view(self):
        """
        Test that worker can be filtered by position
        in list_display on worker admin page.
        """

        position_1 = Position.objects.create(name="PHP Developer")
        position_2 = Position.objects.create(name="Java Developer")

        worker_1 = get_user_model().objects.create_user(
            username="worker1",
            password="worker123",
            position=position_1
        )
        worker_2 = get_user_model().objects.create_user(
            username="worker2",
            password="worker123",
            position=position_2
        )

        url = (
                reverse('admin:task_board_worker_changelist') + "?"
                + urlencode({'position__id__exact': position_1.id})
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, worker_1.username)
        self.assertNotContains(response, worker_2.username)
