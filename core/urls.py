from django.urls import path
from . import views

urlpatterns = [
    # homepage
    path('', views.add_assignment, name='home'),
    # team feature
    path('teams', views.add_team, name='add_team'),
    path('teams/check', views.check_team, name='check_team'),
    path('teams/list', views.list_team, name='list_team'),
    path('teams/delete/<int:id>', views.delete_team, name='delete_team'),
    path('teams/edit/<int:id>', views.edit_team, name='edit_team'),

    # carrier feature
    path('carriers', views.add_carrier, name='add_carrier'),
    path('check_carrier', views.check_carrier, name='check_carrier'),
    path('list_carrier', views.list_carrier, name='list_carrier'),
    path('delete_carrier/<int:id>', views.delete_carrier, name='delete_carrier'),
    path('edit_carrier/<int:id>', views.edit_carrier, name='edit_carrier'),

    # user feature
    path('users', views.add_user, name='add_user'),
    path('check_username', views.check_username, name='check_username'),
    path('list_user', views.list_user, name='list_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('set_password/<int:id>', views.set_password, name='set_password'),

    # task feature
    path('tasks', views.add_task, name='add_task'),
    path('check_task', views.check_task, name='check_task'),
    path('list_task', views.list_task, name='list_task'),
    path('delete_task/<int:id>', views.delete_task, name='delete_task'),
    path('edit_task/<int:id>', views.edit_task, name='edit_task'),

    # assignment feature
    path('assignments', views.add_assignment, name='add_assignment'),
    path('check_assignment', views.check_assignment, name='check_assignment'),
    path('list_assignment', views.list_assignment, name='list_assignment'),
    path('delete_assignment/<int:id>', views.delete_assignment, name='delete_assignment'),
    path('edit_assignment/<int:id>', views.edit_assignment, name='edit_assignment'),

    # vendor feature
    path('vendors', views.add_vendor, name='add_vendor'),
    path('check_vendor', views.check_vendor, name='check_vendor'),
    path('list_vendor', views.list_vendor, name='list_vendor'),
    path('delete_vendor/<int:id>', views.delete_vendor, name='delete_vendor'),
    path('edit_vendor/<int:id>', views.edit_vendor, name='edit_vendor'),

    # employee feature
    path('employees', views.add_employee, name='add_employee'),
    path('check_employee', views.check_employee, name='check_employee'),
    path('list_employee', views.list_employee, name='list_employee'),
    path('delete_employee/<int:id>', views.delete_employee, name='delete_employee'),
    path('edit_employee/<int:id>', views.edit_employee, name='edit_employee'),
]