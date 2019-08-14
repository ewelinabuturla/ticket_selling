from django.db import DatabaseError
from django.http import Http404, HttpResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from tickets.models import (
    Event, 
    Ticket,
    TicketType,
    TicketPurchase
)
from tickets.serializers import (
    EventSerializer,
    TicketsSerializer,
    TicketTypeSerializer,
    TicketPurchaseSerializer
)
from .adapters import charge
from .services import update_tickets_quantity, update_price


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing Events list
    """
    queryset = Event.objects.all().order_by('id')
    serializer_class = EventSerializer
    http_method_names = ['get', ]

class TicketsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing Tickets list
    """
    queryset = Ticket.objects.all().order_by('event')
    serializer_class = TicketsSerializer
    http_method_names = ['get', ]

class TicketTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing TicketType list
    """
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    http_method_names = ['get', ]

class TicketPurchaseAPI(APIView):
    """
    API endpoints to manipulate TicketPurchase
    """

    http_method_names = ['post', ]

    def get(self, request, format=None):
        """
        View list of purchased tickets
        """
        tickets = TicketPurchase.objects.all()
        serializer = TicketPurchaseSerializer(tickets, many=True)
        return Response({"tickets": serializer.data})

    def post(self, request, format=None):
        """
        POST request to purchase a ticket
        """
        serializer = TicketPurchaseSerializer(data=request.data)
        ticket_pk = request.data.get('ticket')
        quantity = int(request.data.get('quantity'))
        bought_ticket = Ticket.objects.get(pk=ticket_pk)
        ticket_amount = int(bought_ticket.ticket_type.amount)

        if (serializer.is_valid(raise_exception=True) and\
            (ticket_amount >= quantity)):
            serializer.save()

            # Update quantity of available tickets. Substract bought ones.
            quantity = -1 * abs(quantity)
            update_tickets_quantity(
                bought_ticket.ticket_type.id,
                quantity,
                ticket_amount
            )

            # Update the final price of the purchase
            update_price(
                request.data.get('email'),
                quantity,
                bought_ticket.ticket_type.price
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif (ticket_amount < quantity):
            # Not enough tickets left
            return HttpResponse('We do not have that many tickets on stock!\
                                Please reduce the number of tickets to buy')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetailAPI(APIView):
    """
    Retrieve, update or delete a purchased ticket instance.
    """

    def get_object(self, pk):
        try:
            return TicketPurchase.objects.get(pk=pk)
        except TicketPurchase.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        """
        Pay for the ticket
        Simplifying the operation I'm assuming
        that I got needed data to proceed
        """
        ticket = self.get_object(pk)
        amount = request.data.get('amount') or ''
        token = request.data.get('token') or ''

        if not ticket.is_expired:
            if ticket.total_price == amount and ticket.status != 'paid':
                ticket.status = 'paid'
                try:
                    ticket.save()
                except DatabaseError as e:
                    return HttpResponse('Could not finish payment properly.\
                                        Please try again')
                return Response(charge(amount, token))
            else:
                return HttpResponse(
                    'Wrong amount of money. Please check the total price'
                )
        else:
            # Free reserved tickets
            return_ticket = Ticket.objects.get(pk=ticket.ticket)
            update_tickets_quantity(
                return_ticket.ticket_type.id,
                ticket.quantity,
                return_ticket.ticket_type.amount
            )
            # Remove related (reserved) ticket
            ticket.delete()
            return HttpResponse('Reservation for the tickets expired')

    def get(self, request, pk, format=None):
        ticket = self.get_object(pk)
        serializer = TicketPurchaseSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        old_ticket = self.get_object(pk)
        serializer = TicketPurchaseSerializer(
            instance=old_ticket,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
