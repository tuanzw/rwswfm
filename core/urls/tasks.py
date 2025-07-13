from django.urls import path
from core.views.task import *

urlpatterns = [
    # task feature
    path('', add_task, name='add_task'),
    path('check/', check_task, name='check_task'),
    path('list/', list_task, name='list_task'),
    path('delete/<int:id>/', delete_task, name='delete_task'),
    path('edit/<int:id>/', edit_task, name='edit_task'),
]