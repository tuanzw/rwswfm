from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import TaskForm
from core.models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task.html'

    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return super().get(request, *args, **kwargs)
        context = self.get_context_data()
        return render(request, 'task.html#task-rows', context)

class TaskAddView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task.html#task-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': '#table_id_task',
            'hx_swap': 'beforeend',
        })
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.name} added successfully!'
        response = render(self.request, 'task.html#task-rows', {'tasks': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task.html#task-form'

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
        response = render(self.request, 'task.html#task-rows', {'tasks': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    # add extra_context in response as overiding form_invalid
    def form_invalid(self, form):
        return super().form_invalid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        self.object.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Task {name} deleted!')
        return response
        
class TaskCheckView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskForm(request.GET)
        response = HttpResponse(as_crispy_field(form['name']))
        trigger = 'frm-has-errors' if form.has_error('name') else 'frm-no-errors'
        return trigger_client_event(response, trigger)