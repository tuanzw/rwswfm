from django.urls import path
from core.views.carrier import *

urlpatterns = [
    # carrier feature
    path('', CarrierListView.as_view(), name='list_carrier'),
    path('add/', CarrierAddView.as_view(), name='add_carrier'),
    path('edit/<int:pk>/', CarrierEditView.as_view(), name='edit_carrier'),
    path('delete/<int:pk>/', CarrierDeleteView.as_view(), name='delete_carrier'),
    path('check/', CarrierCheckView.as_view(), name='check_carrier'),
  ]