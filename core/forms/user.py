from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper

from ..models import User
    
class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    username = forms.CharField(max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'hx-get': reverse_lazy('check_username'),
            'hx-trigger': 'keyup changed delay:1s',
            'hx-target': '#div_id_username',
            'hx-swap': 'outerHTML',
        }))
    
    first_name = forms.CharField(max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'First name'
        }))
    
    last_name = forms.CharField(max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name'
        }))
    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].disabled = True
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False
                
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    
class UserUpdateForm(forms.ModelForm):
    
    username = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].disabled = True
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class SetUserPasswordForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(
        required=True,
        label='New password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        instance = getattr(self, 'instance', None)
        self.username = instance.username
        if instance and instance.pk:
            self.fields['username'].disabled = True

        
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password, User)
        return password

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        user = User.objects.filter(username=self.username).first()
        user.set_password(password)
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ('username', 'password')