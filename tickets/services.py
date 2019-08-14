from django.db import DatabaseError
from rest_framework.response import Response

from .models import TicketType, TicketPurchase


def update_tickets_quantity(pk, quantity, tickets_amount):
    """
    Updates quantity of a give TicketType.

    :param pk: <class 'int'>
    :param quantity: <class 'int'>
    :param tickets_amount: <class 'int'>
    """
    obj = TicketType.objects.get(pk=pk)
    updated_quantity = tickets_amount + quantity
    obj.amount = updated_quantity
    try:
        obj.save()
    except DatabaseError as e:
        Response('Could not update tickets quantity')

def update_price(email, quantity, price):
    """
    Updates final price in TicketPurchase instance. Bases on email which is unique

    :param email: <class 'str'>
    :param quantity: <class 'int'>
    :param price: <class 'float'>
    """
    to_pay = abs(quantity) * price
    obj = TicketPurchase.objects.get(email=email)
    obj.total_price = to_pay
    try:
        obj.save()
    except DatabaseError as e:
        Response('Could not update the final price')
