from django.urls import path
from core.views.team import *

urlpatterns = [
    # team feature
    path('', add_team, name='add_team'),
    path('check/', check_team, name='check_team'),
    path('list/', list_team, name='list_team'),
    path('delete/<int:id>/', delete_team, name='delete_team'),
    path('edit/<int:id>/', edit_team, name='edit_team'),
]