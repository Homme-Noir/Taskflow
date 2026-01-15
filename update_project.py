import os
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent

# Ensure we are in the right place
if not (BASE_DIR / 'manage.py').exists():
    print("Error: manage.py not found. Please run this script from the project root (where manage.py is located).")
    exit(1)

print("Starting Project Update...")

# ------------------------------------------------------------------
# 1. Update tasks/views.py
#    - Adds Search logic to board()
#    - Adds update_task() view
#    - Adds change_status() view
#    - Passes 'today' context for overdue highlighting
# ------------------------------------------------------------------
views_content = """from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Task
from .forms import TaskForm

def board(request):
    query = request.GET.get('q')
    tasks = Task.objects.all().order_by('due_date')
    
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    todos = tasks.filter(status='TODO')
    doing = tasks.filter(status='DOING')
    done = tasks.filter(status='DONE')
    
    return render(request, 'tasks/board.html', {
        'todos': todos, 
        'doing': doing, 
        'done': done,
        'today': timezone.now().date(),
        'query': query or ''
    })

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'New Task'})

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('board')

def change_status(request, pk, status):
    task = get_object_or_404(Task, pk=pk)
    if status in ['TODO', 'DOING', 'DONE']:
        task.status = status
        task.save()
    return redirect('board')
"""

with open(BASE_DIR / 'tasks' / 'views.py', 'w', encoding='utf-8') as f:
    f.write(views_content)
print("✓ Updated tasks/views.py")

# ------------------------------------------------------------------
# 2. Update tasks/urls.py
#    - Adds update_task URL
#    - Adds change_status URL
# ------------------------------------------------------------------
urls_content = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('new/', views.create_task, name='create_task'),
    path('edit/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('status/<int:pk>/<str:status>/', views.change_status, name='change_status'),
]
"""

with open(BASE_DIR / 'tasks' / 'urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)
print("✓ Updated tasks/urls.py")

# ------------------------------------------------------------------
# 3. Update tasks/templates/tasks/board.html
#    - Adds Search Bar
#    - Adds Empty States ({% empty %})
# ------------------------------------------------------------------
board_html_content = """{% extends 'tasks/base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Task Board</h2>
    <div class="d-flex gap-2">
        <form method="get" class="d-flex">
            <input class="form-control me-2" type="search" name="q" placeholder="Search tasks..." value="{{ query }}" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        <a href="{% url 'create_task' %}" class="btn btn-primary text-nowrap">+ Add Task</a>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h5 class="text-secondary fw-bold mb-3">To Do <span class="badge bg-secondary rounded-pill">{{ todos.count }}</span></h5>
        <div class="kanban-col">
            {% for task in todos %} 
                {% include 'tasks/card_partial.html' %} 
            {% empty %}
                <div class="text-center text-muted mt-5">
                    <i class="fas fa-clipboard-list fa-2x mb-2"></i>
                    <p>No tasks to do.</p>
                </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="col-md-4">
        <h5 class="text-primary fw-bold mb-3">In Progress <span class="badge bg-primary rounded-pill">{{ doing.count }}</span></h5>
        <div class="kanban-col">
            {% for task in doing %} 
                {% include 'tasks/card_partial.html' %} 
            {% empty %}
                <div class="text-center text-muted mt-5">
                    <i class="fas fa-spinner fa-2x mb-2"></i>
                    <p>Nothing in progress.</p>
                </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="col-md-4">
        <h5 class="text-success fw-bold mb-3">Done <span class="badge bg-success rounded-pill">{{ done.count }}</span></h5>
        <div class="kanban-col">
            {% for task in done %} 
                {% include 'tasks/card_partial.html' %} 
            {% empty %}
                <div class="text-center text-muted mt-5">
                    <i class="fas fa-check-circle fa-2x mb-2"></i>
                    <p>No completed tasks yet.</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'board.html', 'w', encoding='utf-8') as f:
    f.write(board_html_content)
print("✓ Updated tasks/templates/tasks/board.html")

# ------------------------------------------------------------------
# 4. Update tasks/templates/tasks/card_partial.html
#    - Adds Edit Button
#    - Adds Move Buttons (Start/Done)
#    - Adds Overdue red border logic
# ------------------------------------------------------------------
card_partial_content = """<div class="card task-card p-3 {% if task.due_date < today and task.status != 'DONE' %}border-danger border-2{% endif %}">
    <div class="d-flex justify-content-between mb-2">
        <span class="badge badge-priority-{{ task.priority }} px-2 py-1 rounded-pill" style="font-size: 0.75rem;">
            {{ task.get_priority_display }}
        </span>
        <div>
            <a href="{% url 'update_task' task.pk %}" class="text-muted me-2" title="Edit"><i class="fas fa-pen"></i></a>
            <a href="{% url 'delete_task' task.pk %}" class="text-muted" onclick="return confirm('Delete this task?');" title="Delete"><i class="fas fa-trash"></i></a>
        </div>
    </div>
    <h6 class="fw-bold mb-1">{{ task.title }}</h6>
    <p class="text-muted small mb-3">{{ task.description|truncatechars:50 }}</p>
    
    {% if task.due_date < today and task.status != 'DONE' %}
        <p class="text-danger small fw-bold mb-1"><i class="fas fa-exclamation-circle"></i> Overdue</p>
    {% endif %}

    <div class="d-flex justify-content-between align-items-center border-top pt-2 mt-2">
        <div class="text-muted small"><i class="far fa-clock me-1"></i> {{ task.due_date|date:"M d" }}</div>
        
        <div>
            {% if task.status == 'TODO' %}
                <a href="{% url 'change_status' task.pk 'DOING' %}" class="btn btn-sm btn-outline-primary py-0" style="font-size: 0.75rem;">Start</a>
            {% elif task.status == 'DOING' %}
                <a href="{% url 'change_status' task.pk 'DONE' %}" class="btn btn-sm btn-outline-success py-0" style="font-size: 0.75rem;">Done</a>
            {% elif task.status == 'DONE' %}
                 <a href="{% url 'change_status' task.pk 'TODO' %}" class="text-muted" title="Reopen"><i class="fas fa-undo small"></i></a>
            {% endif %}
        </div>
    </div>
</div>
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'card_partial.html', 'w', encoding='utf-8') as f:
    f.write(card_partial_content)
print("✓ Updated tasks/templates/tasks/card_partial.html")

# ------------------------------------------------------------------
# 5. Update tasks/templates/tasks/task_form.html
#    - Updates header to be dynamic (New vs Edit)
# ------------------------------------------------------------------
task_form_content = """{% extends 'tasks/base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow-sm border-0">
            <div class="card-body p-4">
                <h4 class="mb-3">{{ title|default:"Task" }}</h4>
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary w-100">Save Task</button>
                    <a href="{% url 'board' %}" class="btn btn-light w-100 mt-2">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'task_form.html', 'w', encoding='utf-8') as f:
    f.write(task_form_content)
print("✓ Updated tasks/templates/tasks/task_form.html")

# ------------------------------------------------------------------
# 6. Update tasks/tests.py
#    - Adds basic unit tests
# ------------------------------------------------------------------
tests_content = """from django.test import TestCase
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
"""

with open(BASE_DIR / 'tasks' / 'tests.py', 'w', encoding='utf-8') as f:
    f.write(tests_content)
print("✓ Updated tasks/tests.py")

print("\\nSuccess! All files have been updated.")