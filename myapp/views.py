from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Organization, Role, User
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Handles login page logic
class LoginPage(View):
    # Displays the login page
    def get(self, request):
        return render(request, 'myapp/login.html')
    
    # Handles form submission for login
    def post(self, request):
        username = request.POST.get('username')  # Get username from form
        password = request.POST.get('password')  # Get password from form
        user = authenticate(username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('organization_list')  # Redirect to organization list on success
        else:
            # Show error message if login fails
            messages.error(request, "Email or password is incorrect", extra_tags="alert alert-warning alert-dismissible show")
            return redirect('login')

# Handles user logout
def user_logout(request):
    logout(request)  # Logs the user out
    return redirect('login')  # Redirects to login page

# Displays the list of organizations
@login_required
def organization_list(request):
    main_organizations = None
    sub_organizations = None
    
    # Superusers see all organizations; others see only sub-organizations
    if request.user.is_superuser:
        main_organizations = Organization.objects.all()
    else:
        sub_organizations = Organization.objects.filter(is_main=False)
   
    return render(request, 'myapp/organisation_list.html', {
        'sub_organizations': sub_organizations,
        'main_organizations': main_organizations
    })

# Allows superusers to create main organizations
@login_required
def organization_create(request):
    if not request.user.is_superuser:
        return redirect('organization_list')  # Restrict access for non-superusers

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            org.is_main = True  # Mark as a main organization
            org.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm()
    return render(request, 'myapp/organisation_create.html', {'form': form})

# Allows superusers to create admins for main organizations
@login_required
def organization_admin_create(request):
    if not request.user.is_superuser:
        return redirect('organization_list')

    if request.method == 'POST':
        form = Main_organisation_admin_form(request.POST)
        if form.is_valid():
            user = form.save()  # Save user details
            admin_role, created = Role.objects.get_or_create(name='Admin')  # Assign "Admin" role
            user.role = admin_role
            user.save()
            return redirect('organization_list')
    else:
        form = Main_organisation_admin_form()
    return render(request, 'myapp/main_organisation_admin.html', {'form': form})

# Allows admins to edit main organizations
@login_required
def main_organization_edit(request, id):
    if (not request.user.is_superuser) and (not hasattr(request.user, 'role') or request.user.role.name != 'Admin'):
        return redirect('organization_list')  # Restrict access for non-superusers and non-admins

    obj = Organization.objects.get(id=id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=obj)
        if form.is_valid():
            org = form.save()
            org.main_organisation = request.user.organization
            org.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm(instance=obj)
    return render(request, 'myapp/organisation_create.html', {
        'form': form,
        'title': "Edit main organisation"
    })

# Deletes a main organization
@login_required
def main_organisation_delete(request, id):
    if not request.user.is_superuser:
        return redirect('organization_list') # resctrict to non-superuser
    obj = Organization.objects.get(id=id)
    obj.delete()  # Deletes the organization
    return redirect('organization_list')

# Allows admins to create sub-organizations
@login_required
def sub_organization_create(request):
    if not request.user.role.name == "Admin":
        return redirect('organization_list')  # Restrict access for non-admins

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            org.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm()
    return render(request, 'myapp/organisation_create.html', {
        'form': form,
        'title': "Create sub organization"
    })

# Displays the list of users in the current user's organization
@login_required
def user_list(request):
    if not request.user.role.name == "Admin":
        return HttpResponse('Only organisation admin can see their users')# resctrict access to non-admins
    users = User.objects.filter(organization=request.user.organization)
    return render(request, 'myapp/user_list.html', {'users': users})

# Allows admins to create users
@login_required
def user_create(request):
    if not request.user.role.name == 'Admin':
        return redirect('user_list')  # Restrict access for non-admins

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization  # Assign the current user's organization
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'myapp/user_create.html', {'form': form})

# Allows admins to edit user details
@login_required
def user_edit(request, id):
    if not request.user.role.name == 'Admin':
        return redirect('user_list')  # Restrict access for non-admins

    obj = User.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=obj)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization  # Ensure the user belongs to the same organization
            user.save()
            return redirect('user_list')
    else:
        form = UpdateUserForm(instance=obj)
    return render(request, 'myapp/user_create.html', {'form': form})

# Allows admins to delete users
@login_required
def User_delete(request, id):
    if not request.user.role.name == 'Admin':
        return redirect('organization_list')  # Restrict access for non-admins

    obj = User.objects.get(id=id)
    obj.delete()  # Delete the user
    return redirect('user_list')
