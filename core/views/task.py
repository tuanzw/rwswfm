from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import TaskForm
from core.models import Task
    
@login_required
def add_task(request):
    if not request.htmx:
        return render(request, 'task.html', {'tasks': Task.objects.all()})
    
    # create a modal form for ADDING, set hx_target to the table and hx_swap the beforeend meaning that the added row will be on top
    if request.method == 'GET':
        context = {
            'form': TaskForm(),
            'hx_target': '#table_id_task',
            'hx_swap': 'beforeend',
        }
        return render(request, 'task.html#task-form', context)
    
    # form is valid then swap the whole content here to hx_target and by hx_swap defined
    form = TaskForm(request.POST)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.name} added successfully!'
        response = render(request, 'task.html#task-rows', {'tasks': [obj],})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    
    # form is not valid, so re-define the hx_target and hx_swap
    context = {
        'form': form,
        'hx_target': '#table_id_task',
        'hx_swap': 'beforeend',
    }
    return render(request, 'task.html#task-form', context)

@login_required
def list_task(request):
    return render(request, 'task.html#task-rows', {'tasks': Task.objects.all()})

@login_required
def edit_task(request, id):
    obj = get_object_or_404(Task, pk=id)

    # creating a modal form for EDITING, set the hx_target & hx_swap so that htmx will know
    # where to swap the content after submission
    if request.method == 'GET':
        context = {
            'form': TaskForm(instance=obj),
            'hx_target': f'#row-{obj.id}',
            'hx_swap': 'outerHTML',
        }
        return render(request, 'task.html#task-form', context)
    
    # form is valid then htmx will swap to the hx_target and hx_swap defiend when creating the modal form 
    form = TaskForm(request.POST, instance=obj)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.name} updated successfully!'
        context = {
            'tasks': [obj],
        }
        response = render(request, 'task.html#task-rows', context)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    
    # there is error so re-define hx_target and hx_swap
    context = {
        'form': form,
        'hx_target': f'#row-{obj.id}',
        'hx_swap': 'outerHTML',
    }
    return render(request, 'task.html#task-form', context)
        


def check_task(request):
    form = TaskForm(request.GET)
    response = HttpResponse(as_crispy_field(form['name']))
    trigger = 'frm-has-errors' if form.has_error('name') else 'frm-no-errors'
    return trigger_client_event(response, trigger)
    
    
@login_required
def delete_task(request, id):
    if request.method == 'DELETE':
        obj = get_object_or_404(Task, pk=id)
        obj.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Task {obj.name} deleted!')
        return response