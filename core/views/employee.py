from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import django.db.transaction as transaction
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import EmployeeForm
from core.models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee.html'

    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return super().get(request, *args, **kwargs)
        context = self.get_context_data()
        return render(request, 'employee.html#employee-rows', context)


class EmployeeAddView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee.html#employee-form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        obj = form.save()
        message = f'Employee {obj.user.username} - {obj.user.first_name} {obj.user.last_name} added successfully!'
        
        response = render(self.request, 'employee.html#employee-rows', {'employees': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class EmployeeEditView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee.html#employee-form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': f'#row-{self.object.pk}',
            'hx_swap': 'outerHTML',
        })
        return context

    def form_valid(self, form):
        obj = form.save()
        username = obj.user.username
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        message = f'Employee {username} - {full_name} updated successfully!'
        response = render(self.request, 'employee.html#employee-rows', {'employees': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        response = render(self.request, 'employee.html#employee-form', context)
        # TEMPORARY OVERRIDE: Keep the HTML target as '#row-{pk}', 
        # but safely reroute this specific validation error response into the modal.
        response['HX-Retarget'] = '#dialog'
        response['HX-Reswap'] = 'outerHTML'
        return response


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user  # Grab the linked User instance before deleting anything
        
        username = user.username
        full_name = f"{user.first_name} {user.last_name}".strip()
        
        with transaction.atomic():
            # Deleting the User first will automatically trigger CASCADE and delete the Employee too,
            # but explicitly calling both or letting CASCADE handle it via user.delete() is safer.
            user.delete()
        
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Employee {username} - {full_name} deleted!')
        return response


class EmployeeCheckView(LoginRequiredMixin, View):
    """Optional: Real-time validation (similar to your TeamCheckView)"""
    def get(self, request):
        form = EmployeeForm(request.GET, user=request.user)
        # Check the most likely field to validate (e.g. code)
        response = HttpResponse(as_crispy_field(form['employee_code']))
        trigger = 'frm-has-errors' if form.has_error('employee_code') else 'frm-no-errors'
        return trigger_client_event(response, trigger)