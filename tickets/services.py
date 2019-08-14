from django.db import DatabaseError
from django.http import HttpResponse

from .models import TicketType, TicketPurchase


def update_tickets_quantity(pk, quantity, tickets_amount):
    obj = TicketType.objects.get(pk=pk)
    updated_quantity = tickets_amount + quantity
    obj.amount = updated_quantity
    try:
        obj.save()
    except DatabaseError as e:
        HttpResponse('Could not update tickets quantity')

def update_price(email, quantity, price):
    """
    Update final price.
    Base on email which is unique
    """
    to_pay = abs(quantity) * price
    obj = TicketPurchase.objects.get(email=email)
    obj.total_price = to_pay
    try:
        obj.save()
    except DatabaseError as e:
        HttpResponse('Could not update the final price')
