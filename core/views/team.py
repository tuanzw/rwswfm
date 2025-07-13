from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import TeamForm
from core.models import Team

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'team.html'

    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return super().get(request, *args, **kwargs)
        context = self.get_context_data()
        return render(request, 'team.html#team-rows', context)

class TeamAddView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'team.html#team-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': '#table_id_team',
            'hx_swap': 'beforeend',
        })
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.name} added successfully!'
        response = render(self.request, 'team.html#team-rows', {'teams': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)      
 
class TeamEditView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'team.html#team-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': f'#row-{self.object.pk}',
            'hx_swap': 'outerHTML',
        })
        return context

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.name} updated successfully!'
        response = render(self.request, 'team.html#team-rows', {'teams': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    # add extra_context in response as overiding form_invalid
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, 'team.html#team-form', context)

class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        self.object.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Team {name} deleted!')
        return response

class TeamCheckView(LoginRequiredMixin, View):
    def get(self, request):
        form = TeamForm(request.GET)
        response = HttpResponse(as_crispy_field(form['name']))
        trigger = 'frm-has-errors' if form.has_error('name') else 'frm-no-errors'
        return trigger_client_event(response, trigger)