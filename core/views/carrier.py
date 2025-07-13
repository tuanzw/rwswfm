from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event


from core.forms import CarrierForm
from core.models import Carrier

class CarrierListView(LoginRequiredMixin, ListView):
    model = Carrier
    context_object_name = 'carriers'
    template_name = 'carrier.html'

    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return super().get(request, *args, **kwargs)
        context = self.get_context_data()
        return render(request, 'carrier.html#carrier-rows', context)

class CarrierAddView(LoginRequiredMixin, CreateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'carrier.html#carrier-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': '#table_id_carrier',
            'hx_swap': 'beforeend',
        })
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.carrier} added successfully!'
        response = render(self.request, 'carrier.html#carrier-rows', {'carriers': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class CarrierEditView(LoginRequiredMixin, UpdateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'carrier.html#carrier-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': f'#row-{self.object.pk}',
            'hx_swap': 'outerHTML',
        })
        return context

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.carrier} updated successfully!'
        response = render(self.request, 'carrier.html#carrier-rows', {'carriers': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class CarrierDeleteView(LoginRequiredMixin, DeleteView):
    model = Carrier
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        carrier = self.object.carrier
        self.object.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'Carrier {carrier} deleted!')
        return response

class CarrierCheckView(LoginRequiredMixin, View):
    def get(self, request):
        form = CarrierForm(request.GET)
        response = HttpResponse(as_crispy_field(form['carrier']))
        trigger = 'frm-has-errors' if form.has_error('carrier') else 'frm-no-errors'
        return trigger_client_event(response, trigger)