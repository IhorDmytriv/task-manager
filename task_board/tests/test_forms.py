from datetime import date, timedelta, datetime

from django.test import TestCase

from task_board.forms import (
    WorkerCreationForm,
    WorkerSearchForm,
    NameSearchForm,
    TaskForm,
    TaskSearchForm
)
from task_board.models import Position, Worker, TaskType


class WorkerCreationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Python Developer")
        self.worker_form_data = {
            "username" : "test_user",
            "password1" : "test_password123",
            "password2" : "test_password123",
            "first_name" : "Test",
            "last_name" : "User",
            "email" : "test@mail.com",
            "position" : self.position.id,
        }

    def test_worker_creation_form_with_added_fields(self):
        worker_form = WorkerCreationForm(data=self.worker_form_data)
        self.assertTrue(worker_form.is_valid())
        self.assertEqual(worker_form.cleaned_data["position"], self.position)

    def test_worker_creation_form_creates_worker_object(self):
        worker_form = WorkerCreationForm(data=self.worker_form_data)
        self.assertTrue(worker_form.is_valid())
        worker = worker_form.save()
        self.assertEqual(worker.username, self.worker_form_data["username"])
        self.assertEqual(worker.position, self.position)


class WorkerSearchFormTests(TestCase):
    def test_worker_search_form_has_first_and_last_name_fields(self):
        worker_search_form = WorkerSearchForm()
        self.assertIn("first_name", worker_search_form.fields)
        self.assertIn("last_name", worker_search_form.fields)

    def test_worker_search_form_with_first_and_last_name(self):
        worker_search_form_data = {
            "first_name" : "Test",
            "last_name" : "User",
        }
        worker_search_form = WorkerSearchForm(data=worker_search_form_data)
        self.assertTrue(worker_search_form.is_valid())
        self.assertEqual(worker_search_form.cleaned_data["first_name"], "Test")
        self.assertEqual(worker_search_form.cleaned_data["last_name"], "User")

    def test_worker_search_form_valid_with_empty_username(self):
        worker_search_form = WorkerSearchForm(data={"first_name": "", "last_name": ""})
        self.assertTrue(worker_search_form.is_valid())
        self.assertEqual(worker_search_form.cleaned_data["first_name"], "")
        self.assertEqual(worker_search_form.cleaned_data["last_name"], "")


class NameSearchFormTests(TestCase):
    def test_name_search_form_has_name_field(self):
        name_search_form = NameSearchForm()
        self.assertIn("name", name_search_form.fields)


class TaskCreateFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="New Feature")
        self.worker1 = Worker.objects.create_user(
            username="worker1",
            password="test_password123",
        )
        self.worker2 = Worker.objects.create_user(
            username="worker2",
            password="test_password123",
        )
        self.tomorrow_deadline = (datetime.now().date() + timedelta(days=1))
        self.task_form_data = {
            "name": "Task Title",
            "description": "Description",
            "task_type": self.task_type.id,
            "assignees": [self.worker1.id, self.worker2.id],
            "deadline": self.tomorrow_deadline,
            "priority": 2
        }

    def test_task_create_form_valid_and_cleans_all_fields(self):
        task_form = TaskForm(data=self.task_form_data)
        self.assertTrue(task_form.is_valid())

        self.assertEqual(task_form.cleaned_data["task_type"], self.task_type)
        self.assertEqual(task_form.cleaned_data["deadline"], self.tomorrow_deadline)
        self.assertEqual(task_form.cleaned_data["priority"], 2)

        list_assignees = list(task_form.cleaned_data["assignees"])
        self.assertEqual(list_assignees, [self.worker1, self.worker2])

    def test_task_create_form_invalid_when_deadline_in_past(self):
        invalid_data = self.task_form_data.copy()
        yesterday_deadline = datetime.now().date() - timedelta(days=1)
        invalid_data["deadline"] = yesterday_deadline
        task_form = TaskForm(data=invalid_data)

        self.assertFalse(task_form.is_valid())
        self.assertIn("deadline", task_form.errors)
        self.assertEqual(task_form.errors["deadline"], ["Deadline cannot be in the past."])

    def test_task_create_form_priority_field_uses_radioselect(self):
        task_form = TaskForm()
        widget = task_form.fields["priority"].widget
        from django.forms.widgets import RadioSelect
        self.assertIsInstance(widget, RadioSelect)

    def test_task_name_search_form_has_name_field(self):
        task_name_search_form = TaskSearchForm()
        self.assertIn("name", task_name_search_form.fields)
