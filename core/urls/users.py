from django.urls import path
from core.views.user import *

urlpatterns = [
    # user feature
    path('', add_user, name='add_user'),
    path('check/', check_username, name='check_username'),
    path('list/', list_user, name='list_user'),
    path('delete/<int:id>/', delete_user, name='delete_user'),
    path('edit/<int:id>/', edit_user, name='edit_user'),
    path('set_password/<int:id>/', set_password, name='set_password'),
]