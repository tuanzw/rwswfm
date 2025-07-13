from django.urls import path
from core.views.task import *

urlpatterns = [
    # task feature
    path('', TaskListView.as_view(), name='list_task'),
    path('add/', TaskAddView.as_view(), name='add_task'),
    path('edit/<int:pk>/', TaskEditView.as_view(), name='edit_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('check/', TaskCheckView.as_view(), name='check_task'),

]