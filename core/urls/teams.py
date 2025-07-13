from django.urls import path
from core.views.team import *

urlpatterns = [
    # team feature
    path('', TeamListView.as_view(), name='list_team'),
    path('add/', TeamAddView.as_view(), name='add_team'),
    path('edit/<int:pk>/', TeamEditView.as_view(), name='edit_team'),
    path('delete/<int:pk>/', TeamDeleteView.as_view(), name='delete_team'),
    path('check/', TeamCheckView.as_view(), name='check_team'),
]