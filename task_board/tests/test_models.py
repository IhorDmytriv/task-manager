from django.test import TestCase

from task_board.models import Position, Worker, TaskType, Task


class ModelTests(TestCase):
    # setUp
    def setUp(self):
        self.position = Position.objects.create(name="Python Developer")
        self.task_type = TaskType.objects.create(name="New Feature")

    # Position Tests
    def test_position_str(self):
        position = self.position
        self.assertEqual(str(position), "Python Developer")

    # Worker Tests
    def test_create_worker_with_position_and_str(self):
        username = "test_worker"
        first_name = "Test"
        last_name = "Worker"
        password = "test123"
        worker = Worker.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            position=self.position,
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position, self.position)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(
            str(worker),
            f"{worker.first_name}, {worker.last_name}, ({worker.username})"
        )

    # TaskType Tests
    def test_task_type_str(self):
        task_type = self.task_type
        self.assertEqual(str(task_type), self.task_type.name)

    # Task Tests
    def test_task_str(self):
        task = Task.objects.create(
            task_type=self.task_type,
            name="Add sign-in with Google button",
            priority=3,
        )
        self.assertEqual(
            str(task),
            f"{task.name} ({task.get_priority_display()})"
        )

    def test_task_priority_default_choice(self):
        task = Task.objects.create(
            task_type=self.task_type,
        )
        self.assertEqual(task.get_priority_display(), "Medium Priority")

    def test_task_priority_can_be_changed(self):
        task = Task.objects.create(
            task_type=self.task_type,
            priority=1,
        )
        self.assertEqual(task.get_priority_display(), "Low Priority")

    def test_task_deadline_is_optional(self):
        task = Task.objects.create(
            task_type=self.task_type,
            name="Task without deadline"
        )
        self.assertIsNone(task.deadline)

    def test_task_is_complete_default(self):
        task = Task.objects.create(
            task_type=self.task_type,
            name="Some task"
        )
        self.assertFalse(task.is_complete)

    def test_task_assignees(self):
        worker1 = Worker.objects.create_user(
            username="Worker1",
            password="test123",
            position=self.position
        )
        worker2 = Worker.objects.create_user(
            username="Worker2",
            password="test123",
            position=self.position
        )
        task = Task.objects.create(
            task_type=self.task_type,
            name="Task with assignees"
        )

        task.assignees.set([worker1, worker2])
        self.assertIn(worker1, task.assignees.all())
        self.assertIn(worker2, task.assignees.all())

    def test_task_has_no_assignees_by_default(self):
        task = Task.objects.create(
            task_type=self.task_type,
            name="Unassigned task"
        )
        self.assertEqual(task.assignees.count(), 0)
