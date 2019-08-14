from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import (
    TicketType,
    Ticket,
    Event,
    TicketPurchase
)
from ..serializers import TicketTypeSerializer

# Initialize the APIClient app
client = Client()


class TicketsTest(TestCase):
    """
    Test module for API requests
    """
    def setUp(self):
        self.ticket_type_1 = TicketType.objects.create(
            id=4,
            ticket_type='VIP ticket',
            amount=100,
            price=150
        )
        self.ticket_type_2 = TicketType.objects.create(
            id=5,
            ticket_type='Regular ticket',
            amount=80,
            price=100
        )
        self.ticket_type_3 = TicketType.objects.create(
            id=6,
            ticket_type='Normal ticket',
            amount=50,
            price=30
        )
        self.event_1 = Event.objects.create(
            id=3,
            name='Piano concert',
            description='Live piano music',
            time='2019-08-09T19:06:19Z'
        )
        self.event_2 = Event.objects.create(
            id=4,
            name='Hip-hop music',
            description='Hip-hop show!',
            time='2019-08-19T19:06:19Z'
        )
        self.ticket_1 = Ticket.objects.create(
            id=4,
            event=self.event_1,
            ticket_type=self.ticket_type_1
        )
        self.ticket_2 = Ticket.objects.create(
            id=5,
            event=self.event_2,
            ticket_type=self.ticket_type_2
        )
        self.ticket_3 = Ticket.objects.create(
            id=6,
            event=self.event_2,
            ticket_type=self.ticket_type_3
        )
        self.purchase_ticket_1 = TicketPurchase.objects.create(
            id=3,
            date='2019-08-09T19:06:19Z',
            quantity=10,
            ticket=1,
            email='some-email@email.com',
            total_price=1500
        )
        self.purchase_tickt_2 = TicketPurchase.objects.create(
            id=4,
            date='2019-08-09T19:06:19Z',
            quantity=1,
            ticket=2,
            email='another-emil@email.com',
            total_price=200
        )

    def test_get_all_ticket_types(self):
        # API response
        response = client.get(
            reverse('tickettype-list')
        )
        # DB data
        ticket_types = TicketType.objects.all()
        serializer = TicketTypeSerializer(ticket_types, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_get_ticket_type_4(self):
        # API response
        response = client.get(
            reverse('tickettype-detail', kwargs={'pk': 4}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            dict(response.json()),
            {
                'id': 4,
                'ticket_type': 'VIP ticket',
                'amount': 100,
                'price': '150.00'
            }
        )

    def test_forbidden_post_ticket_type(self):
        """
        Make sure that TicketType can't be created
        via API.
        This should be allowed only from admin panel
        """
        response = self.client.post(
            reverse('tickettype-list'),
            {
                'ticket_type': 'Test ticket',
                'amount': 20,
                'price': 100
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_forbidden_delete_ticket_type(self):
        """
        Make sure that TicketType can't be deleted
        via API.
        This should be allowed only from admin panel
        """
        response = self.client.delete(
            reverse('tickettype-detail', kwargs={'pk': 4}),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_forbidden_get_purchased_ticket_list(self):
        """
        Make sure that list of all purchased tickets can't
        be viewed via API.
        This should be allowed only from admin panel
        """
        response = self.client.get(
            reverse('api:purchase'),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_post_purchased_ticket(self):
        response = self.client.post(
            reverse('api:purchase'),
            {
                'ticket': 4,
                'quantity': 10,
                'email': 'email-test@test.pl'
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
