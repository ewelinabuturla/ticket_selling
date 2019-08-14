from django.db import DatabaseError
from django.http import Http404
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
            return Response('We do not have that many tickets on stock!\
                                Please reduce the number of tickets to buy')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetailAPI(APIView):
    """
    Retrieve, update or delete a purchased ticket instance.
    """
    http_method_names = ['post', 'put', 'get', ]

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
                # At this point would be best to disable PUT method
                ticket.status = 'paid'
                try:
                    ticket.save()
                except DatabaseError as e:
                    return Response('Could not finish payment properly.\
                                        Please try again')
                return Response(charge(amount, token))
            else:
                return Response(
                    'Ticker already paid or wrong amount of money.\
                    Please check the total price'
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
            return Response('Reservation for the tickets expired')

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
        if serializer.is_valid(raise_exception=True) and\
           not old_ticket.is_expired and old_ticket.status == 'pending':
            if request.data.get('quantity'):
                # Check if tickets are availeble
                # Update the price and quantity
                bought_ticket = Ticket.objects.get(pk=old_ticket.ticket)
                ticket_amount = int(bought_ticket.ticket_type.amount)
                request_quantity = int(request.data.get('quantity'))
                difference = old_ticket.quantity - request_quantity

                if ticket_amount >= difference:
                    serializer.save()
                    # Update the final price
                    update_price(
                        old_ticket.email,
                        request_quantity,
                        bought_ticket.ticket_type.price
                    )
                    # Update the tickets amount
                    update_tickets_quantity(
                        bought_ticket.ticket_type.id,
                        difference,
                        ticket_amount
                    )
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    Response('There is no enough tickets! Sorry')
            elif request.data.get('email'):
                # Change email value
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('Not valid operation')
        else:
            return Response('Not valid operation!')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
