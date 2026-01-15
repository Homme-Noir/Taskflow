from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="TODO",
            priority="MEDIUM",
            due_date=timezone.now().date()
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(str(self.task), "Test Task")

class TaskViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="View Test Task",
            status="TODO",
            due_date=timezone.now().date()
        )

    def test_board_view_status_code(self):
        response = self.client.get(reverse('board'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Task")

    def test_update_task_status(self):
        url = reverse('change_status', args=[self.task.id, 'DOING'])
        response = self.client.get(url)
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 302) # Redirects
        self.assertEqual(self.task.status, 'DOING')
