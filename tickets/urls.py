from django.urls import path

from .views import TicketPurchaseAPI, TicketDetailAPI

app_name = 'api'

urlpatterns = [
    path(r'ticket/purchase/', TicketPurchaseAPI.as_view(), name='purchase'),
    path(r'ticket/purchase/<int:pk>', TicketDetailAPI.as_view(), name='purchase-detail'),
]
