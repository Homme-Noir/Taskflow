from django.shortcuts import render, redirect, get_object_or_404
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
