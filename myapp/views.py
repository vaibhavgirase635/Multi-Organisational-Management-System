# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Organization, Role, User
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class LoginPage(View):
    def get(self, request):
        
        return render(request, 'myapp/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
            # print(password)
        user = authenticate(username=username,password=password)
        print(user)
        
        if user is not None:
            login(request,user)
            
            return redirect('organization_list') 
        else:
            messages.error(request, "Email or password is incorrect", extra_tags="alert alert-warning alert-dismissible show")
            return redirect('login')
        
def user_logout(request):
    logout(request)
    return redirect('login')
@login_required
def organization_list(request):
    print(request.user)
    main_organizations = None
    sub_organizations = None
    
    if request.user.is_superuser:
        main_organizations = Organization.objects.all()
    else:
        sub_organizations = Organization.objects.filter(is_main=False)
   
    return render(request, 'myapp/organisation_list.html', {'sub_organizations': sub_organizations,'main_organizations':main_organizations})

@login_required
def organization_create(request):
    if not request.user.is_superuser:
        return redirect('organization_list')

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            org.is_main = True
            org.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm()
    return render(request, 'myapp/organisation_create.html', {'form': form})

@login_required
def organization_admin_create(request):
    if not request.user.is_superuser:
        return redirect('organization_list')

    if request.method == 'POST':
        form = Main_organisation_admin_form(request.POST)
        if form.is_valid():
            user = form.save()
            admin_role, created = Role.objects.get_or_create(name='Admin')
            user.role = admin_role
            user.save()
            return redirect('organization_list')
    else:
        form = Main_organisation_admin_form()
    return render(request, 'myapp/main_organisation_admin.html', {'form': form})

@login_required
def main_organization_edit(request,id):
    if (not request.user.is_superuser) and (not hasattr(request.user, 'role') or request.user.role.name != 'Admin'):
        return redirect('organization_list')

    obj = Organization.objects.get(id=id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST,instance=obj)
        if form.is_valid():
            org = form.save()
            org.main_organisation = request.user.organization
            org.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm(instance=obj)
    return render(request, 'myapp/organisation_create.html', {'form': form,'title':"Edit main organisation"})

@login_required
def main_organisation_delete(request,id):
    obj = Organization.objects.get(id=id)
    obj.delete()
    return redirect('organization_list')
@login_required
def sub_organization_create(request):
    if not request.user.role.name == "Admin":
        return redirect('organization_list')

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            
            org.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm()
    return render(request, 'myapp/organisation_create.html', {'form': form,'title':"Create sub organisation"})




@login_required
def user_list(request):
    users = User.objects.filter(organization=request.user.organization)
    return render(request, 'myapp/user_list.html', {'users': users})

@login_required
def user_create(request):
    if not request.user.role.name == 'Admin':
        return redirect('user_list')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'myapp/user_create.html', {'form': form})

@login_required
def user_edit(request,id):
    if not request.user.role.name == 'Admin':
        return redirect('user_list')
    obj = User.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST,instance=obj)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization
            user.save()
            return redirect('user_list')
    else:
        form = UpdateUserForm(instance=obj)
    return render(request, 'myapp/user_create.html', {'form': form})

@login_required
def User_delete(request,id):
    if not request.user.role.name == 'Admin':
        return redirect('organization_list')
    obj = User.objects.get(id=id)
    obj.delete()
    return redirect('user_list')