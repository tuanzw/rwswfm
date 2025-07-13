from django.urls import path
from core.views.user import *

urlpatterns = [
    # user feature
    path('', UserListView.as_view(), name='list_user'),
    path('add/', UserAddView.as_view(), name='add_user'),
    path('edit/<int:pk>/', UserEditView.as_view(), name='edit_user'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('check/', UserCheckView.as_view(), name='check_username'),
    path('set_password/<int:pk>/', UserSetPasswordView.as_view(), name='set_password'),
]