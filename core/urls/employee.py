from django.urls import path
from core.views.employee import *
from core.views.team import TeamListView

urlpatterns = [
    # Employee URLs
    path('', EmployeeListView.as_view(), name='list_employee'),
    path('add/', EmployeeAddView.as_view(), name='add_employee'),
    path('edit/<int:pk>/', EmployeeEditView.as_view(), name='edit_employee'),
    path('delete/<int:pk>/', EmployeeDeleteView.as_view(), name='delete_employee'),
    path('check/', EmployeeCheckView.as_view(), name='check_employee'),
]