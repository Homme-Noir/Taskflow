from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def board(request):
    tasks = Task.objects.all().order_by('due_date')
    todos = tasks.filter(status='TODO')
    doing = tasks.filter(status='DOING')
    done = tasks.filter(status='DONE')
    
    return render(request, 'tasks/board.html', {
        'todos': todos, 
        'doing': doing, 
        'done': done
    })

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('board')
