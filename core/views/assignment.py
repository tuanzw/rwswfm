from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import AssignmentForm
from ..models import Assignment

    
@login_required
def add_assignment(request):
    if not request.htmx:
        assignments = Assignment.objects.all()
        context = {'assignments': assignments}
        return render(request, 'assignment.html', context)
    else:
        if request.method == 'GET':
            context = {'form': AssignmentForm(user=request.user)}
            return render(request, 'assignment.html#assignment-form', context)
        elif request.method == 'POST':
            form = AssignmentForm(request.POST, user=request.user)
            if form.is_valid():
                assignment = form.save()
                message = f'{assignment.empid} added successfully!'
                context = {'assignments': [assignment],}
                response = render(request, 'assignment.html#assignment-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'assignment.html#assignment-form', context)

@login_required
def list_assignment(request):
    if request.method == 'GET':
        assignments = Assignment.objects.all()
        context = {'assignments': assignments}
        return render(request, 'assignment.html#assignment-rows', context)

@login_required
def edit_assignment(request, id):
    if request.method == 'GET':
        assignment = get_object_or_404(Assignment, pk=id)
        assignment_frm = AssignmentForm(instance=assignment, user=request.user)
        context = {'form': assignment_frm}
        return render(request, 'assignment.html#assignment-form', context)
    elif request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=id)
        form = AssignmentForm(request.POST, instance=assignment, user=request.user)
        if form.is_valid():
            assignment = form.save()
            message = f'{assignment.empid} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'assignment.html#assignment-form', context)
        

def check_assignment(request):
    assignment_frm = AssignmentForm(request.GET)
    response = HttpResponse(as_crispy_field(assignment_frm['name']))
    if assignment_frm.has_error('name'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    
@login_required
def delete_assignment(request, id):
    if request.method == 'DELETE':
        assignment = Assignment.objects.filter(pk=id).first()
        assignment.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'Assignment {assignment.empid} deleted!',
            })
        })