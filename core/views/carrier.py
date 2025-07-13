from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event


from core.forms import CarrierForm
from core.models import Carrier

@login_required
def add_carrier(request):
    if not request.htmx:
        return render(request, 'carrier.html', {'carriers': Carrier.objects.all()})
    if request.method == 'GET':
        context = {
            'form': CarrierForm(),
            'hx_target': '#table_id_carrier',
            'hx_swap': 'beforeend',
        }
        return render(request, 'carrier.html#carrier-form', context)
    form = CarrierForm(request.POST)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.carrier} added successfully!'
        response = render(request, 'carrier.html#carrier-rows', {'carriers': [obj],})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    
    context = {
        'form': form,
        'hx_target': '#table_id_carrier',
        'hx_swap': 'beforeend',
    }
    return render(request, 'carrier.html#carrier-form', context)

@login_required
def list_carrier(request):
    return render(request, 'carrier.html#carrier-rows', {'carriers': Carrier.objects.all()})

@login_required
def edit_carrier(request, id):
    obj = get_object_or_404(Carrier, pk=id)
    if request.method == 'GET':
        context = {
            'form': CarrierForm(instance=obj),
            'hx_target': f'#row-{obj.id}',
            'hx_swap': 'outerHTML',
        }
        return render(request, 'carrier.html#carrier-form', context)
    form = CarrierForm(request.POST, instance=obj)
    if form.is_valid():
        obj = form.save()
        message = f'{obj.carrier} updated successfully!'
        context = {
            'carriers': [obj],
        }
        response = render(request, 'carrier.html#carrier-rows', context)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response
    context = {
        'form': form,
        'hx_target': f'#row-{obj.id}',
        'hx_swap': 'outerHTML',
    }
    return render(request, 'carrier.html#carrier-form', context)
        


def check_carrier(request):
    form = CarrierForm(request.GET)
    response = HttpResponse(as_crispy_field(form['carrier']))
    trigger = 'frm-has-errors' if form.has_error('carrier') else 'frm-no-errors'
    return trigger_client_event(response, trigger)
    
    
@login_required
def delete_carrier(request, id):
    if request.method == 'DELETE':
        obj = get_object_or_404(Carrier, pk=id)
        obj.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Carrier {obj.carrier} deleted!')
        return response