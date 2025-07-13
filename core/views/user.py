from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import UserForm, UserUpdateForm, SetUserPasswordForm
from core.models import User

@login_required()
def list_user(request):
    return render(request, 'user.html#user-rows', {'users': User.objects.all()})

@login_required
def add_user(request):
    if not request.htmx:
        return render(request, 'user.html', {'users': User.objects.all()})
    if request.method == 'GET':
        context = {
            'form': UserForm(),
            'hx_target': '#table_id_user',
            'hx_swap': 'beforeend',
        }
        return render(request, 'user.html#user-form', context)
    
    form = UserForm(request.POST)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.username} added successfully!'
        response = render(request, 'user.html#user-rows', {'users': [obj],})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    
    context = {
        'form': form,
        'hx_target': '#table_id_user',
        'hx_swap': 'beforeend',
    }
    return render(request, 'user.html#user-form', context)

@login_required
def edit_user(request, id):
    obj = get_object_or_404(User, pk=id)
    if request.method == 'GET':
        context = {
            'form': UserUpdateForm(instance=obj),
            'hx_target': f'#row-{obj.id}',
            'hx_swap': 'outerHTML',
        }
        return render(request, 'user.html#user-form', context)
    form = UserUpdateForm(request.POST, instance=obj)
    if form.is_valid():
        obj = form.save()
        context = {
            'users': [obj]
        }
        message = f'{obj.username} updated successfully!'
        response = render(request, 'user.html#user-rows', context)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    
    context = {
        'form': form,
        'hx_target': f'#row-{obj.id}',
        'hx_swap': 'outerHTML',
    }
    return render(request, 'user.html#user-form', context)

@login_required
def delete_user(request, id):
    if request.method == 'DELETE':
        obj = get_object_or_404(User, pk=id)
        obj.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'User {obj.username} deleted!')
        return response

def check_username(request):
    form = UserForm(request.GET)
    response = HttpResponse(as_crispy_field(form['username']))
    trigger = 'frm-has-errors' if form.has_error('username') else 'frm-no-errors'
    return trigger_client_event(response, trigger)

def set_password(request, id):
    obj = get_object_or_404(User, pk=id)
    if request.method == 'GET':
        context = {
            'form': SetUserPasswordForm(instance=obj),
            'hx_target': f'#row-{obj.id}',
            'hx_swap': 'outerHTML',
        }
        return render(request, 'user.html#user-form', context)
    
    form = SetUserPasswordForm(request.POST, instance=obj)
    if form.is_valid():
        context = {
            'users': [obj],
        }
        response = render(request, 'user.html#user-rows', context)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Password for {obj.username} changed successfully!')
        return response

    context = {
        'form': form,
        'hx_target': f'#row-{obj.id}',
        'hx_swap': 'outerHTML',
    }
    return render(request, 'user.html#user-form', context)