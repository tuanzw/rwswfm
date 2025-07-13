from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from core.forms import UserForm, UserUpdateForm, SetUserPasswordForm
from core.models import User

class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return super().get(request, *args, **kwargs)
        context = self.get_context_data()
        return render(request, 'user.html#user-rows', context)

class UserAddView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user.html#user-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': '#table_id_user',
            'hx_swap': 'beforeend',
        })
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.username} added successfully!'
        response = render(self.request, 'user.html#user-rows', {'users': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user.html#user-form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hx_target': f'#row-{self.object.pk}',
            'hx_swap': 'outerHTML',
        })
        return context

    def form_valid(self, form):
        obj = form.save()
        message = f'{obj.username} updated successfully!'
        response = render(self.request, 'user.html#user-rows', {'users': [obj]})
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', message)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        username = self.object.username
        self.object.delete()
        response = HttpResponse(status=200)
        response = trigger_client_event(response, 'on-success')
        response = trigger_client_event(response, 'showMessage', f'User {username} deleted!')

class UserCheckView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserForm(request.GET)
        response = HttpResponse(as_crispy_field(form['username']))
        trigger = 'frm-has-errors' if form.has_error('username') else 'frm-no-errors'
        return trigger_client_event(response, trigger)

class UserSetPasswordView(LoginRequiredMixin, View):
    model = User
    form_class = SetUserPasswordForm
    template_name = 'user.html#user-form'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = kwargs
        context.update({
            'hx_target': f'#row-{self.object.pk}',
            'hx_swap': 'outerHTML',
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(form=self.form_class(instance=self.object))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            context = {
                'users': [self.object],
            }
            response = render(request, 'user.html#user-rows', context)
            response = trigger_client_event(response, 'on-success')
            response = trigger_client_event(response, 'showMessage', f'Password for {self.object.username} changed successfully!')
            return response
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)