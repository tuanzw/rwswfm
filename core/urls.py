from django.urls import path
from . import views

urlpatterns = [
    # homepage
    path('', views.add_team, name='home'),
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
]