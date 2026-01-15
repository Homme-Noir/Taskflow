import os
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent

if not (BASE_DIR / 'manage.py').exists():
    print("Error: manage.py not found. Please run this from the project root.")
    exit(1)

print("Starting UI Upgrade to 'Modern Clean' Theme...")

# ------------------------------------------------------------------
# 1. Update BASE.HTML
#    - Adds Google Font 'Inter'
#    - Adds Custom CSS for Sidebar, Cards, Buttons, and Layout
# ------------------------------------------------------------------
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskFlow</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --primary-color: #4f46e5; /* Indigo */
            --primary-hover: #4338ca;
            --secondary-bg: #f3f4f6;
            --sidebar-bg: #1e293b; /* Slate 800 */
            --sidebar-text: #cbd5e1;
            --sidebar-hover: #334155;
            --card-bg: #ffffff;
            --text-main: #1f2937;
            --text-muted: #6b7280;
        }

        body {
            background-color: var(--secondary-bg);
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
            overflow-x: hidden;
        }

        /* --- Sidebar --- */
        .sidebar {
            height: 100vh;
            background-color: var(--sidebar-bg);
            width: 260px;
            position: fixed;
            top: 0;
            left: 0;
            display: flex;
            flex-direction: column;
            padding-top: 1.5rem;
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .sidebar-brand {
            color: #fff;
            font-weight: 700;
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
            letter-spacing: -0.5px;
        }

        .sidebar-brand i { color: var(--primary-color); }

        .sidebar a {
            color: var(--sidebar-text);
            text-decoration: none;
            padding: 0.85rem 1.5rem;
            display: flex;
            align-items: center;
            font-weight: 500;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }

        .sidebar a:hover, .sidebar a.active {
            background-color: var(--sidebar-hover);
            color: #fff;
            border-left-color: var(--primary-color);
        }
        
        .sidebar a i { width: 25px; text-align: center; margin-right: 10px; }

        .sidebar-footer {
            margin-top: auto;
            padding: 1.5rem;
            border-top: 1px solid #334155;
            background: rgba(0,0,0,0.1);
        }

        /* --- Main Content --- */
        .main-content {
            margin-left: 260px;
            padding: 2rem;
            min-height: 100vh;
        }

        /* Responsive Layout for Mobile */
        @media (max-width: 768px) {
            .sidebar { transform: translateX(-100%); }
            .main-content { margin-left: 0; }
        }

        /* --- Components --- */
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: all 0.2s;
        }
        .btn-primary:hover {
            background-color: var(--primary-hover);
            border-color: var(--primary-hover);
            transform: translateY(-1px);
        }

        /* --- Card Styling --- */
        .task-card {
            background: var(--card-bg);
            border: none;
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .task-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Priority Strips */
        .task-card.priority-HIGH { border-left: 4px solid #ef4444; }
        .task-card.priority-MEDIUM { border-left: 4px solid #f59e0b; }
        .task-card.priority-LOW { border-left: 4px solid #10b981; }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* Auth Container */
        .auth-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        }
    </style>
</head>
<body>

    {% if user.is_authenticated %}
    <div class="sidebar">
        <div class="sidebar-brand">
            <i class="fas fa-check-double me-2"></i>TaskFlow
        </div>
        
        <div class="mt-3">
            <a href="{% url 'board' %}" class="{% if request.resolver_match.url_name == 'board' %}active{% endif %}">
                <i class="fas fa-columns"></i> Board
            </a>
            <a href="{% url 'create_task' %}" class="{% if request.resolver_match.url_name == 'create_task' %}active{% endif %}">
                <i class="fas fa-plus-circle"></i> New Task
            </a>
        </div>
        
        <div class="sidebar-footer">
            <div class="d-flex align-items-center mb-3">
                <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px;">
                    {{ user.username|make_list|first|upper }}
                </div>
                <div class="overflow-hidden">
                    <small class="d-block text-muted" style="font-size: 0.75rem;">Signed in as</small>
                    <div class="text-truncate text-white fw-bold" style="max-width: 140px;">{{ user.username }}</div>
                </div>
            </div>
            <form action="{% url 'logout' %}" method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-outline-secondary btn-sm w-100 text-light border-secondary hover-white">
                    <i class="fas fa-sign-out-alt me-1"></i> Logout
                </button>
            </form>
        </div>
    </div>
    {% endif %}

    <div class="{% if user.is_authenticated %}main-content{% else %}auth-container{% endif %}">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'base.html', 'w', encoding='utf-8') as f:
    f.write(base_html)
print("✓ Updated base.html (New CSS, Sidebar, Google Fonts)")

# ------------------------------------------------------------------
# 2. Update BOARD.HTML
#    - Improved header layout
#    - Better empty states
#    - Responsive Grid
# ------------------------------------------------------------------
board_html = """{% extends 'tasks/base.html' %}
{% block content %}
<div class="container-fluid p-0">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5">
        <div>
            <h2 class="fw-bold mb-1 text-dark">Project Board</h2>
            <p class="text-muted mb-0">Manage your tasks and track progress.</p>
        </div>
        
        <div class="d-flex gap-3 mt-3 mt-md-0">
            <form method="get" class="position-relative">
                <i class="fas fa-search position-absolute text-muted" style="left: 15px; top: 12px;"></i>
                <input class="form-control ps-5 rounded-pill border-0 shadow-sm" style="min-width: 250px;" 
                       type="search" name="q" placeholder="Search tasks..." value="{{ query }}">
            </form>
            <a href="{% url 'create_task' %}" class="btn btn-primary rounded-pill px-4 d-flex align-items-center shadow-sm">
                <i class="fas fa-plus me-2"></i> Add Task
            </a>
        </div>
    </div>

    <div class="row g-4">
        
        <div class="col-md-4">
            <div class="d-flex align-items-center justify-content-between mb-3 px-1">
                <h6 class="text-uppercase fw-bold text-secondary mb-0 tracking-wide" style="letter-spacing: 1px; font-size: 0.85rem;">
                    <i class="fas fa-circle text-secondary me-2" style="font-size: 8px;"></i>To Do
                </h6>
                <span class="badge bg-white text-dark border shadow-sm rounded-pill px-3">{{ todos.count }}</span>
            </div>
            <div class="kanban-col bg-light rounded-4 p-2 h-100" style="min-height: 500px; background: #f8fafc;">
                {% for task in todos %} 
                    {% include 'tasks/card_partial.html' %} 
                {% empty %}
                    <div class="text-center text-muted mt-5 opacity-50">
                        <i class="far fa-clipboard fa-3x mb-3"></i>
                        <p class="small">No tasks to do</p>
                    </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="d-flex align-items-center justify-content-between mb-3 px-1">
                <h6 class="text-uppercase fw-bold text-primary mb-0 tracking-wide" style="letter-spacing: 1px; font-size: 0.85rem;">
                    <i class="fas fa-circle text-primary me-2" style="font-size: 8px;"></i>In Progress
                </h6>
                <span class="badge bg-white text-dark border shadow-sm rounded-pill px-3">{{ doing.count }}</span>
            </div>
            <div class="kanban-col bg-light rounded-4 p-2 h-100" style="min-height: 500px; background: #eff6ff;">
                {% for task in doing %} 
                    {% include 'tasks/card_partial.html' %} 
                {% empty %}
                    <div class="text-center text-muted mt-5 opacity-50">
                        <i class="fas fa-spinner fa-3x mb-3"></i>
                        <p class="small">Nothing in progress</p>
                    </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="d-flex align-items-center justify-content-between mb-3 px-1">
                <h6 class="text-uppercase fw-bold text-success mb-0 tracking-wide" style="letter-spacing: 1px; font-size: 0.85rem;">
                    <i class="fas fa-circle text-success me-2" style="font-size: 8px;"></i>Done
                </h6>
                <span class="badge bg-white text-dark border shadow-sm rounded-pill px-3">{{ done.count }}</span>
            </div>
            <div class="kanban-col bg-light rounded-4 p-2 h-100" style="min-height: 500px; background: #f0fdf4;">
                {% for task in done %} 
                    {% include 'tasks/card_partial.html' %} 
                {% empty %}
                    <div class="text-center text-muted mt-5 opacity-50">
                        <i class="far fa-check-circle fa-3x mb-3"></i>
                        <p class="small">No completed tasks</p>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'board.html', 'w', encoding='utf-8') as f:
    f.write(board_html)
print("✓ Updated board.html (Cleaner layout, nicer columns)")

# ------------------------------------------------------------------
# 3. Update CARD_PARTIAL.HTML
#    - New Priority Logic (Colored Border)
#    - Cleaner typography
#    - Better Action Buttons
# ------------------------------------------------------------------
card_partial = """<div class="card task-card p-3 mb-3 priority-{{ task.priority }}">
    <div class="d-flex justify-content-between align-items-start mb-2">
        <span class="badge rounded-pill fw-normal 
            {% if task.priority == 'HIGH' %}bg-danger-subtle text-danger
            {% elif task.priority == 'MEDIUM' %}bg-warning-subtle text-warning-emphasis
            {% else %}bg-success-subtle text-success{% endif %}" style="font-size: 0.7rem;">
            {{ task.get_priority_display }}
        </span>
        
        <div class="dropdown">
            <button class="btn btn-link text-muted p-0 no-arrow" type="button" data-bs-toggle="dropdown">
                <i class="fas fa-ellipsis-h"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0">
                <li><a class="dropdown-item small" href="{% url 'update_task' task.pk %}"><i class="fas fa-pen me-2 text-primary"></i> Edit</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item small text-danger" href="{% url 'delete_task' task.pk %}" onclick="return confirm('Delete this task?');"><i class="fas fa-trash me-2"></i> Delete</a></li>
            </ul>
        </div>
    </div>

    <h6 class="fw-bold mb-1 text-dark">{{ task.title }}</h6>
    <p class="text-muted small mb-3" style="font-size: 0.85rem; line-height: 1.4;">{{ task.description|truncatechars:60 }}</p>

    <div class="d-flex justify-content-between align-items-center pt-2 mt-auto border-top border-light">
        <div class="text-muted small d-flex align-items-center {% if task.due_date < today and task.status != 'DONE' %}text-danger fw-bold{% endif %}">
            <i class="far fa-calendar-alt me-1"></i> 
            {{ task.due_date|date:"M d" }}
        </div>

        <div class="d-flex gap-1">
            {% if task.status == 'TODO' %}
                <a href="{% url 'change_status' task.pk 'DOING' %}" class="btn btn-sm btn-light text-primary rounded-circle" title="Start Task" style="width: 30px; height: 30px; padding: 0; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-play" style="font-size: 0.7rem;"></i>
                </a>
            {% elif task.status == 'DOING' %}
                <a href="{% url 'change_status' task.pk 'DONE' %}" class="btn btn-sm btn-light text-success rounded-circle" title="Mark Done" style="width: 30px; height: 30px; padding: 0; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-check" style="font-size: 0.8rem;"></i>
                </a>
            {% elif task.status == 'DONE' %}
                 <a href="{% url 'change_status' task.pk 'TODO' %}" class="btn btn-sm btn-light text-secondary rounded-circle" title="Reopen" style="width: 30px; height: 30px; padding: 0; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-undo" style="font-size: 0.7rem;"></i>
                </a>
            {% endif %}
        </div>
    </div>
</div>
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'card_partial.html', 'w', encoding='utf-8') as f:
    f.write(card_partial)
print("✓ Updated card_partial.html (Added Priority Strips, Dropdown menu)")

# ------------------------------------------------------------------
# 4. Update FORMS (Signup, Login, Create)
#    - Centered Cards
#    - Clean inputs
# ------------------------------------------------------------------
# Common CSS for forms to make them look nice (injected via base, but specific structure here)

login_html = """{% extends 'tasks/base.html' %}
{% block content %}
<div class="card shadow-lg border-0 rounded-4" style="width: 100%; max-width: 400px;">
    <div class="card-body p-5">
        <div class="text-center mb-4">
            <div class="bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
                <i class="fas fa-user-circle fa-2x"></i>
            </div>
            <h3 class="fw-bold">Welcome Back</h3>
            <p class="text-muted small">Login to manage your workflow</p>
        </div>

        <form method="post">
            {% csrf_token %}
            {% for field in form %}
            <div class="mb-3">
                <label class="form-label small fw-bold text-uppercase text-muted">{{ field.label }}</label>
                {{ field }}
            </div>
            {% endfor %}
            <button type="submit" class="btn btn-primary w-100 py-2 rounded-3 fw-bold mt-2">Log In</button>
        </form>
        
        <div class="text-center mt-4">
            <p class="small text-muted">New here? <a href="{% url 'signup' %}" class="text-primary fw-bold text-decoration-none">Create an account</a></p>
        </div>
    </div>
</div>
"""

signup_html = """{% extends 'tasks/base.html' %}
{% block content %}
<div class="card shadow-lg border-0 rounded-4" style="width: 100%; max-width: 400px;">
    <div class="card-body p-5">
        <div class="text-center mb-4">
            <div class="bg-success bg-opacity-10 text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
                <i class="fas fa-rocket fa-2x"></i>
            </div>
            <h3 class="fw-bold">Get Started</h3>
            <p class="text-muted small">Create your account for free</p>
        </div>

        <form method="post">
            {% csrf_token %}
            {% for field in form %}
            <div class="mb-3">
                <label class="form-label small fw-bold text-uppercase text-muted">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                <div class="form-text small">{{ field.help_text }}</div>
                {% endif %}
            </div>
            {% endfor %}
            <button type="submit" class="btn btn-success w-100 py-2 rounded-3 fw-bold mt-2">Sign Up</button>
        </form>
        
        <div class="text-center mt-4">
            <p class="small text-muted">Already have an account? <a href="{% url 'login' %}" class="text-primary fw-bold text-decoration-none">Log in</a></p>
        </div>
    </div>
</div>
"""

# Need to update task_form to match the centered/card style but inside the dashboard
task_form_html = """{% extends 'tasks/base.html' %}
{% block content %}
<div class="container h-100 d-flex justify-content-center align-items-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow-sm border-0 rounded-4">
            <div class="card-header bg-white border-0 pt-4 pb-0 px-4">
                <h4 class="fw-bold">{{ title|default:"Task" }}</h4>
            </div>
            <div class="card-body p-4">
                <form method="post">
                    {% csrf_token %}
                    
                    {{ form.as_p }}
                    
                    <div class="d-flex gap-2 mt-4">
                        <button type="submit" class="btn btn-primary px-4 rounded-3">Save Task</button>
                        <a href="{% url 'board' %}" class="btn btn-light px-4 rounded-3 text-muted">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open(BASE_DIR / 'tasks' / 'templates' / 'registration' / 'login.html', 'w', encoding='utf-8') as f:
    f.write(login_html)

with open(BASE_DIR / 'tasks' / 'templates' / 'registration' / 'signup.html', 'w', encoding='utf-8') as f:
    f.write(signup_html)

with open(BASE_DIR / 'tasks' / 'templates' / 'tasks' / 'task_form.html', 'w', encoding='utf-8') as f:
    f.write(task_form_html)
print("✓ Updated Forms (Login, Signup, Task Form)")

print("\n-------------------------------------------------------------")
print("SUCCESS! UI has been upgraded.")
print("Run 'python manage.py runserver' to see the new look.")
print("-------------------------------------------------------------")