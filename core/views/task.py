from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import TaskForm
from ..models import Task

    
@login_required
def add_task(request):
    if not request.htmx:
        tasks = Task.objects.all()
        context = {'tasks': tasks}
        return render(request, 'task.html', context)
    else:
        if request.method == 'GET':
            context = {'form': TaskForm()}
            return render(request, 'task.html#task-form', context)
        elif request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save()
                message = f'{task.name} added successfully!'
                context = {'tasks': [task],}
                response = render(request, 'task.html#task-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'task.html#task-form', context)

@login_required
def list_task(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        context = {'tasks': tasks}
        return render(request, 'task.html#task-rows', context)

@login_required
def edit_task(request, id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=id)
        task_frm = TaskForm(instance=task)
        context = {'form': task_frm}
        return render(request, 'task.html#task-form', context)
    elif request.method == 'POST':
        task = get_object_or_404(Task, pk=id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            message = f'{task.name} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'task.html#task-form', context)
        

def check_task(request):
    task_frm = TaskForm(request.GET)
    response = HttpResponse(as_crispy_field(task_frm['name']))
    if task_frm.has_error('name'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    
@login_required
def delete_task(request, id):
    if request.method == 'DELETE':
        task = Task.objects.filter(pk=id).first()
        task.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'Task {task.name} deleted!',
            })
        })