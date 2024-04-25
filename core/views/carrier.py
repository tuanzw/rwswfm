from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import CarrierForm
from ..models import Carrier

    
@login_required
def add_carrier(request):
    if not request.htmx:
        carriers = Carrier.objects.all()
        context = {'carriers': carriers}
        return render(request, 'carrier.html', context)
    else:
        if request.method == 'GET':
            context = {'form': CarrierForm()}
            return render(request, 'carrier.html#carrier-form', context)
        elif request.method == 'POST':
            form = CarrierForm(request.POST)
            if form.is_valid():
                carrier = form.save()
                message = f'{carrier.carrier} added successfully!'
                context = {'carriers': [carrier],}
                response = render(request, 'carrier.html#carrier-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'carrier.html#carrier-form', context)

@login_required
def list_carrier(request):
    if request.method == 'GET':
        carriers = Carrier.objects.all()
        context = {'carriers': carriers}
        return render(request, 'carrier.html#carrier-rows', context)

@login_required
def edit_carrier(request, id):
    if request.method == 'GET':
        carrier = get_object_or_404(Carrier, pk=id)
        carrier_frm = CarrierForm(instance=carrier)
        context = {'form': carrier_frm}
        return render(request, 'carrier.html#carrier-form', context)
    elif request.method == 'POST':
        print(request.POST)
        carrier = get_object_or_404(Carrier, pk=id)
        form = CarrierForm(request.POST, instance=carrier)
        if form.is_valid():
            carrier = form.save()
            message = f'{carrier.carrier} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'carrier.html#carrier-form', context)
        


def check_carrier(request):
    carrier_frm = CarrierForm(request.GET)
    response = HttpResponse(as_crispy_field(carrier_frm['carrier']))
    if carrier_frm.has_error('carrier'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    
@login_required
def delete_carrier(request, id):
    if request.method == 'DELETE':
        carrier = Carrier.objects.filter(pk=id).first()
        carrier.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'Carrier {carrier.carrier} deleted!',
            })
        })