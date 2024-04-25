from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import TeamForm
from ..models import Team

    
@login_required
def add_team(request):
    if not request.htmx:
        teams = Team.objects.all()
        context = {'teams': teams}
        return render(request, 'team.html', context)
    else:
        if request.method == 'GET':
            context = {'form': TeamForm()}
            return render(request, 'team.html#team-form', context)
        elif request.method == 'POST':
            form = TeamForm(request.POST)
            if form.is_valid():
                team = form.save()
                message = f'{team.name} added successfully!'
                context = {'teams': [team],}
                response = render(request, 'team.html#team-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'team.html#team-form', context)

@login_required
def list_team(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        context = {'teams': teams}
        return render(request, 'team.html#team-rows', context)

@login_required
def edit_team(request, id):
    if request.method == 'GET':
        team = get_object_or_404(Team, pk=id)
        team_frm = TeamForm(instance=team)
        context = {'form': team_frm}
        return render(request, 'team.html#team-form', context)
    elif request.method == 'POST':
        team = get_object_or_404(Team, pk=id)
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save()
            message = f'{team.name} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'team.html#team-form', context)
        

def check_team(request):
    team_frm = TeamForm(request.GET)
    response = HttpResponse(as_crispy_field(team_frm['name']))
    if team_frm.has_error('name'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    
@login_required
def delete_team(request, id):
    if request.method == 'DELETE':
        team = Team.objects.filter(pk=id).first()
        team.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'Team {team.name} deleted!',
            })
        })