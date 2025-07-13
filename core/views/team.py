from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import TeamForm
from core.models import Team

@login_required
def add_team(request):
    if not request.htmx:
        return render(request, 'team.html', {'teams': Team.objects.all()})
    if request.method == 'GET':
        context = {
            'form': TeamForm(),
            'hx_target': '#table_id_team',
            'hx_swap': 'beforeend',
        }
        return render(request, 'team.html#team-form', context)
    form = TeamForm(request.POST)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.name} added successfully!'
        response = render(request, 'team.html#team-rows', {'teams': [obj],})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    
    context = {
        'form': form,
        'hx_target': '#table_id_team',
        'hx_swap': 'beforeend',
    }
    return render(request, 'team.html#team-form', context)

@login_required
def list_team(request):
    return render(request, 'team.html#team-rows', {'teams': Team.objects.all()})

@login_required
def edit_team(request, id):
    obj = get_object_or_404(Team, pk=id)
    if request.method == 'GET':
        context = {
            'form': TeamForm(instance=obj),
            'hx_target': f'#row-{obj.id}',
            'hx_swap': 'outerHTML',
        }
        return render(request, 'team.html#team-form', context)
    form = TeamForm(request.POST, instance=obj)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.name} updated successfully!'
        context = {
            'teams': [obj],
        }
        response = render(request, 'team.html#team-rows', context)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    context = {
        'form': form,
        'hx_target': f'#row-{obj.id}',
        'hx_swap': 'outerHTML',
    }
    return render(request, 'team.html#team-form', context)
        

def check_team(request):
    form = TeamForm(request.GET)
    response = HttpResponse(as_crispy_field(form['name']))
    trigger = 'frm-has-errors' if form.has_error('name') else 'frm-no-errors'
    return trigger_client_event(response, trigger)
    
    
@login_required
def delete_team(request, id):
    if request.method == 'DELETE':
        obj = get_object_or_404(Team, pk=id)
        obj.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Team {obj.name} deleted!')
        return response