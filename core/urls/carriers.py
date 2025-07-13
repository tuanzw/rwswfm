from django.urls import path
from core.views.carrier import *

urlpatterns = [
    # carrier feature
    path('', add_carrier, name='add_carrier'),
    path('check/', check_carrier, name='check_carrier'),
    path('list/', list_carrier, name='list_carrier'),
    path('delete/<int:id>/', delete_carrier, name='delete_carrier'),
    path('edit/<int:id>/', edit_carrier, name='edit_carrier'),
]