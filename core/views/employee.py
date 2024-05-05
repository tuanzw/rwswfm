from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import EmployeeForm
from ..models import Employee

    
@login_required
def add_employee(request):
    if not request.htmx:
        employees = Employee.objects.all()
        context = {'employees': employees}
        return render(request, 'employee.html', context)
    else:
        if request.method == 'GET':
            context = {'form': EmployeeForm()}
            return render(request, 'employee.html#employee-form', context)
        elif request.method == 'POST':
            form = EmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save()
                message = f'{employee.empid} added successfully!'
                context = {'employees': [employee],}
                response = render(request, 'employee.html#employee-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'employee.html#employee-form', context)

@login_required
def list_employee(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        context = {'employees': employees}
        return render(request, 'employee.html#employee-rows', context)

@login_required
def edit_employee(request, id):
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=id)
        employee_frm = EmployeeForm(instance=employee)
        context = {'form': employee_frm}
        return render(request, 'employee.html#employee-form', context)
    elif request.method == 'POST':
        employee = get_object_or_404(Employee, pk=id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            message = f'{employee.empid} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'employee.html#employee-form', context)
        

def check_employee(request):
    employee_frm = EmployeeForm(request.GET)
    response = HttpResponse(as_crispy_field(employee_frm['empid']))
    if employee_frm.has_error('empid'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    
@login_required
def delete_employee(request, id):
    if request.method == 'DELETE':
        employee = Employee.objects.filter(pk=id).first()
        employee.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'employee {employee.empid} deleted!',
            })
        })