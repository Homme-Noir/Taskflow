from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('board')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def board(request):
    query = request.GET.get('q')
    # Filter tasks ONLY for the logged-in user
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    
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

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign current user
            task.save()
            return redirect('board')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'New Task'})

@login_required
def update_task(request, pk):
    # Ensure user owns the task
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('board')

@login_required
def change_status(request, pk, status):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if status in ['TODO', 'DOING', 'DONE']:
        task.status = status
        task.save()
    return redirect('board')
