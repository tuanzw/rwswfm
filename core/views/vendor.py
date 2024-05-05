from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import VendorForm
from ..models import Vendor

    
@login_required
def add_vendor(request):
    if not request.htmx:
        vendors = Vendor.objects.all()
        context = {'vendors': vendors}
        return render(request, 'vendor.html', context)
    else:
        if request.method == 'GET':
            context = {'form': VendorForm()}
            return render(request, 'vendor.html#vendor-form', context)
        elif request.method == 'POST':
            form = VendorForm(request.POST)
            if form.is_valid():
                vendor = form.save()
                message = f'{vendor.name} added successfully!'
                context = {'vendors': [vendor],}
                response = render(request, 'vendor.html#vendor-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'vendor.html#vendor-form', context)

@login_required
def list_vendor(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        context = {'vendors': vendors}
        return render(request, 'vendor.html#vendor-rows', context)

@login_required
def edit_vendor(request, id):
    if request.method == 'GET':
        vendor = get_object_or_404(Vendor, pk=id)
        vendor_frm = VendorForm(instance=vendor)
        context = {'form': vendor_frm}
        return render(request, 'vendor.html#vendor-form', context)
    elif request.method == 'POST':
        vendor = get_object_or_404(Vendor, pk=id)
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save()
            message = f'{vendor.name} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            return response
        context = {'form': form}
        return render(request, 'vendor.html#vendor-form', context)
        

def check_vendor(request):
    vendor_frm = VendorForm(request.GET)
    response = HttpResponse(as_crispy_field(vendor_frm['name']))
    if vendor_frm.has_error('name'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    
@login_required
def delete_vendor(request, id):
    if request.method == 'DELETE':
        vendor = Vendor.objects.filter(pk=id).first()
        vendor.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'vendor {vendor.name} deleted!',
            })
        })