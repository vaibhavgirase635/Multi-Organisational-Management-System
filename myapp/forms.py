# forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                   'adress':forms.Textarea(attrs={'class':'form-control'})}

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role','password1','password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.EmailInput(attrs={'class':'form-control'}),
                   'role':forms.Select(attrs={'class':'form-control'}),
                   'password1':forms.PasswordInput(attrs={'class':'form-control'}),
                   'password2':forms.PasswordInput(attrs={'class':'form-control'})}

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.EmailInput(attrs={'class':'form-control'}),
                   'role':forms.Select(attrs={'class':'form-control'})}
        
class Main_organisation_admin_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'organization','password1','password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.EmailInput(attrs={'class':'form-control'}),
                   'organisation':forms.TextInput(attrs={'class':'form-control'}),
                   'password1':forms.PasswordInput(attrs={'class':'form-control'}),
                   'password2':forms.PasswordInput(attrs={'class':'form-control'})}



        
