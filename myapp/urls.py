
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/create/', views.organization_create, name='organization_create'),
    path('main-organization-edit/<int:id>/', views.main_organization_edit, name='main_organization_edit'),
    path('main-organization-delete/<int:id>/', views.main_organisation_delete, name='main_organisation_delete'),
    path('sub-organization-create/', views.sub_organization_create, name='sub_organization_create'),
    path('organization-admin-create/', views.organization_admin_create, name='organization_admin_create'),
    
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:id>/', views.User_delete, name='user_delete'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
