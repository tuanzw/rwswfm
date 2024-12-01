from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import AttendanceForm
from ..models import Attendance

    
@login_required
def add_attendance(request):
    if not request.htmx:
        attendances = Attendance.objects.all().select_related('empid')
        context = {'attendances': attendances}
        return render(request, 'attendance.html', context)
    else:
        if request.method == 'GET':
            context = {'form': AttendanceForm()}
            return render(request, 'attendance.html#attendance-form', context)
        elif request.method == 'POST':
            form = AttendanceForm(request.POST)
            if form.is_valid():
                attendance = form.save()
                message = f'{attendance.empid} added successfully!'
                context = {'attendances': [attendance],}
                response = render(request, 'attendance.html#attendance-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'attendance.html#attendance-form', context)

@login_required
def list_attendance(request):
    if request.method == 'GET':
        attendances = Attendance.objects.all()
        context = {'attendances': attendances}
        return render(request, 'attendance.html#attendance-rows', context)

@login_required
def edit_attendance(request, id):
    if request.method == 'GET':
        attendance = get_object_or_404(Attendance, pk=id)
        attendance_frm = AttendanceForm(instance=attendance)
        context = {'form': attendance_frm}
        return render(request, 'attendance.html#attendance-form', context)
    elif request.method == 'POST':
        attendance = get_object_or_404(Attendance, pk=id)
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save()
            message = f'{attendance.empid} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'attendance.html#attendance-form', context)
    
    
@login_required
def delete_attendance(request, id):
    if request.method == 'DELETE':
        attendance = Attendance.objects.filter(pk=id).first()
        attendance.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'Attendance {attendance.empid} deleted!',
            })
        })