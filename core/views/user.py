from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import UserForm, UserUpdateForm, SetUserPasswordForm
from ..models import User

@login_required()
def list_user(request):
    if request.method == 'GET':
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'user.html#user-rows', context)

@login_required
def add_user(request):
    if not request.htmx:
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'user.html', context)
    else:
        if request.method == 'GET':
            context = {'form': UserForm()}
            return render(request, 'user.html#user-form', context)
        elif request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                message = f'{user.username} added successfully!'
                context = {'users': [user],}
                response = render(request, 'user.html#user-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'user.html#user-form', context)

@login_required
def edit_user(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=id)
        user_frm = UserUpdateForm(instance=user)
        context = {'form': user_frm}
        return render(request, 'user.html#user-form', context)
    elif request.method == 'POST':
        user = get_object_or_404(User, pk=id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            context = {'user': user}
            message = f'{user.username} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            print(response.headers)
            return response
        print(form.errors)
        context = {'form': form}
        return render(request, 'user.html#user-form', context)

@login_required
def delete_user(request, id):
    if request.method == 'DELETE':
        user = User.objects.filter(pk=id).first()
        user.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'showMessage': f'User {user.username} deleted!',
            })
        })
def check_username(request):
    user_frm = UserForm(request.GET)
    response = HttpResponse(as_crispy_field(user_frm['username']))
    if user_frm.has_error('username'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')

def set_password(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=id)
        user_frm = SetUserPasswordForm(instance=user)
        print(user)
        context = {'form': user_frm}
        return render(request, 'user.html#user-form', context)
    elif request.method == 'POST':
        print(request.POST)
        user = get_object_or_404(User, pk=id)
        form = SetUserPasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            context = {'user': user}
            message = f'Password for {user.username} changed successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'on-success': None,
                    'showMessage': message
                })
            })
            print(response.headers)
            return response
        print(form.errors)
        context = {'form': form}
        return render(request, 'user.html#user-form', context)